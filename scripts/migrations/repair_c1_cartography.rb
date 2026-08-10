#!/usr/bin/env ruby
# frozen_string_literal: true

require 'yaml'
require 'json'
require 'date'
require 'pathname'

ROOT = Pathname.new(Dir.pwd).realpath
LOCATIONS = ROOT + 'locations'
MANIFEST = ROOT + 'website/content/public/manifest.json'
PRESENTATION = ROOT + 'website/content/public/archive-presentation.json'
FRONTMATTER = /\A---\s*\n(.*?)\n---\s*\n(.*)\z/m


def normalize_dates(value)
  case value
  when Date, Time, DateTime then value.strftime('%Y-%m-%d')
  when Hash then value.to_h { |key, child| [key.to_s, normalize_dates(child)] }
  when Array then value.map { |child| normalize_dates(child) }
  else value
  end
end


def parse_record(path)
  source = File.read(path, encoding: 'UTF-8')
  match = FRONTMATTER.match(source)
  raise "#{path}: missing YAML front matter" unless match
  meta = YAML.safe_load(match[1], permitted_classes: [Date, Time, DateTime], aliases: false) || {}
  [normalize_dates(meta), match[2]]
end


def dump_record(path, meta, body)
  yaml = YAML.dump(meta, line_width: -1).sub(/\A---\s*\n/, '')
  File.write(path, "---\n#{yaml}---\n#{body}", encoding: 'UTF-8')
end

legacy_manifest = JSON.parse(File.read(MANIFEST, encoding: 'UTF-8'))
legacy_presentation = JSON.parse(File.read(PRESENTATION, encoding: 'UTF-8'))
legacy_by_id = legacy_manifest.fetch('entries').to_h { |entry| [entry.fetch('id'), entry] }

records_by_slug = {}
Dir.glob((LOCATIONS + '*.md').to_s).sort.each do |path|
  next if File.basename(path) == 'README.md'
  meta, body = parse_record(path)
  next unless meta['schema_version'] == 1 && meta['record_type'] == 'location'
  records_by_slug[meta.fetch('slug')] = [path, meta, body]
end

repairs = []
legacy_presentation.fetch('mapEntries').each do |map_entry|
  legacy = legacy_by_id.fetch(map_entry.fetch('id'))
  record_tuple = records_by_slug[legacy.fetch('slug')]
  raise "No Schema v1 location owns approved C1 slug #{legacy['slug']}" unless record_tuple

  path, meta, body = record_tuple
  marker = map_entry.fetch('mapMarker')
  expected_category = marker.match?(/\A[A-F]\z/) ? 'restricted' : 'numbered'
  cartography = Array(meta['cartography'])
  canonical = cartography.find do |candidate|
    candidate['map_id'] == 'aetherhaven-city' && candidate['category'] != 'unlisted'
  end

  if canonical
    unless canonical['category'] == expected_category && canonical['reference'].to_s == marker
      raise "#{meta['id']}: canonical cartography conflicts with approved C1 map: expected #{expected_category} #{marker}, found #{canonical['category']} #{canonical['reference']}"
    end
    next
  end

  cartography << {
    'map_id' => 'aetherhaven-city',
    'category' => expected_category,
    'reference' => marker
  }
  meta['cartography'] = cartography
  dump_record(path, meta, body)
  repairs << "#{meta['id']}=#{marker}"
end

puts JSON.pretty_generate(repaired: repairs, count: repairs.length)
