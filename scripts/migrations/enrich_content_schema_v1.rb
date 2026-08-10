#!/usr/bin/env ruby
# frozen_string_literal: true

require 'yaml'
require 'date'
require 'pathname'
require 'open3'
require 'json'

ROOT = Pathname.new(Dir.pwd).realpath
ROOTS = %w[characters locations organizations artifacts vessels historical_events story_drafts story_arcs].freeze

EXTRA_RELATION_FIELDS = {
  'character' => {
    'primary_location' => 'primary-location',
    'key_relationships' => 'connected-to',
    'affiliation' => 'affiliated-with',
    'public_affiliation' => 'affiliated-with',
    'possible_connection' => 'possible-connection',
    'known_to' => 'known-to',
    'unknown_to' => 'unknown-to',
    'signature_artifact' => 'signature-artifact'
  },
  'location' => {
    'primary_guardian' => 'guarded-by',
    'key_connections' => 'connected-to'
  },
  'organization' => {
    'known_leadership' => 'led-by',
    'primary_connections' => 'related-to',
    'governing_body' => 'governed-by',
    'meeting_place' => 'meets-at',
    'modern_federation' => 'federated-as',
    'member_guilds' => 'has-member',
    'seat' => 'seated-at',
    'presiding_officer' => 'presided-by'
  }
}.freeze

Record = Struct.new(:path, :meta, :body, keyword_init: true)

REPORT = {
  relationships_added: [],
  fields_fully_modeled: [],
  fields_partially_modeled: [],
  character_asset_roles_corrected: [],
  catalog_numbers_corrected: [],
  story_chronology_corrected: []
}

def normalize_dates(value)
  case value
  when Date, Time, DateTime then value.strftime('%Y-%m-%d')
  when Hash then value.to_h { |k, v| [k.to_s, normalize_dates(v)] }
  when Array then value.map { |v| normalize_dates(v) }
  else value
  end
end

def parse_markdown_text(text, label)
  match = text.match(/\A---\s*\n(.*?)\n---\s*\n(.*)\z/m)
  raise "#{label}: missing YAML front matter" unless match
  yaml = match[1].gsub(/^aliases:\[\]\s*$/, 'aliases: []')
  meta = YAML.safe_load(yaml, permitted_classes: [Date, Time, DateTime], aliases: false) || {}
  [normalize_dates(meta), match[2]]
end

def load_record(path)
  meta, body = parse_markdown_text(File.read(ROOT + path, encoding: 'UTF-8'), path)
  Record.new(path: Pathname.new(path), meta: meta, body: body)
end

def dump_record(record)
  yaml = YAML.dump(record.meta, line_width: -1).sub(/\A---\s*\n/, '')
  File.write(ROOT + record.path, "---\n#{yaml}---\n#{record.body}", encoding: 'UTF-8')
end

def listify(value)
  return [] if value.nil? || value == '' || value == []
  value.is_a?(Array) ? value.compact : [value]
end

def normalize_name(value)
  value.to_s.downcase.gsub(/[“”]/, '"').gsub(/[’'`]/, '').gsub(/&/, ' and ').gsub(/[^a-z0-9]+/, ' ').strip.gsub(/\s+/, ' ')
end

def original_meta(path)
  stdout, status = Open3.capture2('git', 'show', "origin/main:#{path}")
  return nil unless status.success?
  parse_markdown_text(stdout, "origin/main:#{path}").first
rescue StandardError
  nil
end

def build_lookup(records)
  lookup = Hash.new { |h, k| h[k] = [] }
  path_lookup = {}
  records.each do |record|
    id = record.meta.fetch('id')
    path_lookup[record.path.to_s] = id
    names = [record.meta['name'], *listify(record.meta['aliases']), record.path.basename('.md').to_s.tr('_', ' ')]
    names.each do |value|
      key = normalize_name(value)
      next if key.empty?
      lookup[key] << id unless lookup[key].include?(id)
      if key.start_with?('the ')
        short = key.sub(/\Athe\s+/, '')
        lookup[short] << id unless lookup[short].include?(id)
      end
    end
  end
  [lookup, path_lookup]
end

def resolve_name(value, name_lookup)
  return nil unless value.is_a?(String)
  raw = value.strip
  return nil if raw.empty?
  candidates = [raw]
  candidates << raw.split(',', 2).first if raw.include?(',')
  candidates << raw.gsub(/\s*\([^)]*\)\s*/, ' ').strip if raw.include?('(')
  candidates.uniq.each do |candidate|
    ids = name_lookup[normalize_name(candidate)]
    return ids.first if ids&.length == 1
  end
  nil
end

def add_relationship!(record, target, type)
  return false if target.nil? || target == record.meta['id']
  relationships = record.meta['relationships'] ||= []
  return false if relationships.any? { |r| r['target'] == target && r['type'] == type }
  relationships << { 'target' => target, 'type' => type, 'visibility' => 'story-sensitive' }
  REPORT[:relationships_added] << { path: record.path.to_s, target: target, type: type }
  true
end

def remove_preservation_field!(record, field)
  marker = '## Schema Migration Preservation Notes'
  return unless record.body.include?(marker)
  before, section = record.body.split(marker, 2)
  lines = section.lines
  pattern = /^- \*\*#{Regexp.escape(field)}:\*\*/
  lines.reject! { |line| line.match?(pattern) }
  has_entries = lines.any? { |line| line.start_with?('- **') }
  record.body = if has_entries
                  before.rstrip + "\n\n#{marker}\n" + lines.join.sub(/\A\s*\n/, "\n")
                else
                  before.rstrip + "\n"
                end
end

def exact_catalog_number(body)
  patterns = [
    /CATALOG\s+No\.?\*{0,2}\s*[:\-]?\s*`([A-Z]{1,8}-\d+-\d{3})`/i,
    /CATALOG\s+No\.?\*{0,2}\s*[:\-]?\s*([A-Z]{1,8}-\d+-\d{3})(?:\s|$)/i
  ]
  patterns.each do |pattern|
    match = body.match(pattern)
    return match[1].upcase if match
  end
  nil
end

records = ROOTS.flat_map do |root|
  dir = ROOT + root
  next [] unless dir.directory?
  Dir.glob((dir + '*.md').to_s).sort.filter_map do |absolute|
    next if File.basename(absolute) == 'README.md'
    relative = Pathname.new(absolute).relative_path_from(ROOT).to_s
    record = load_record(relative)
    next unless record.meta['schema_version'] == 1
    record
  end
end

name_lookup, = build_lookup(records)

records.each do |record|
  legacy = original_meta(record.path.to_s)
  type = record.meta['record_type']

  # Legacy character images were visual references, not typed portraits. Do not invent portrait semantics.
  if type == 'character'
    listify(record.meta['assets']).each do |asset|
      next unless asset['role'] == 'portrait'
      asset['role'] = 'reference'
      asset['alt'] = "Canonical visual reference for #{record.meta['name']}."
      REPORT[:character_asset_roles_corrected] << { path: record.path.to_s, asset: asset['id'] }
    end
  end

  # Story-draft chronology strings are relative placement metadata unless the source explicitly models a different state later.
  if type == 'story' && record.meta['chronology'].is_a?(Hash) && record.meta['chronology']['status'] != 'relative'
    record.meta['chronology']['status'] = 'relative'
    REPORT[:story_chronology_corrected] << record.path.to_s
  end

  # Catalog numbers are accepted only when an exact in-body identifier is visible.
  if type == 'artifact' && record.meta['artifact'].is_a?(Hash)
    current = record.meta['artifact']['catalog_number']
    exact = exact_catalog_number(record.body)
    if exact && current != exact
      record.meta['artifact']['catalog_number'] = exact
      REPORT[:catalog_numbers_corrected] << { path: record.path.to_s, from: current, to: exact }
    elsif current && (current.include?("\n") || current.length > 64)
      record.meta['artifact'].delete('catalog_number')
      REPORT[:catalog_numbers_corrected] << { path: record.path.to_s, from: current, to: nil }
    end
  end

  next unless legacy

  # Fold legacy access phrases into the Version 1 location access list without changing their wording.
  if type == 'location'
    extra_access = listify(legacy['public_access']) + listify(legacy['actual_access'])
    unless extra_access.empty?
      record.meta['location'] ||= {}
      record.meta['location']['access_status'] ||= []
      extra_access.map(&:to_s).each { |value| record.meta['location']['access_status'] << value unless record.meta['location']['access_status'].include?(value) }
      remove_preservation_field!(record, 'public_access') if legacy.key?('public_access')
      remove_preservation_field!(record, 'actual_access') if legacy.key?('actual_access')
      REPORT[:fields_fully_modeled] << { path: record.path.to_s, field: 'public_access/actual_access' }
    end
  end

  # Preserve safe explicit character metadata in the defined character extension.
  if type == 'character'
    record.meta['character'] ||= {}
    if legacy['formal_title']
      record.meta['character']['titles'] ||= []
      listify(legacy['formal_title']).map(&:to_s).each { |value| record.meta['character']['titles'] << value unless record.meta['character']['titles'].include?(value) }
      remove_preservation_field!(record, 'formal_title')
      REPORT[:fields_fully_modeled] << { path: record.path.to_s, field: 'formal_title' }
    end
    if legacy['apparent_age'] && !record.meta['character']['age_status']
      record.meta['character']['age_status'] = listify(legacy['apparent_age']).map(&:to_s).join('; ')
      remove_preservation_field!(record, 'apparent_age')
      REPORT[:fields_fully_modeled] << { path: record.path.to_s, field: 'apparent_age' }
    end
  end

  (EXTRA_RELATION_FIELDS[type] || {}).each do |field, relation_type|
    values = listify(legacy[field])
    next if values.empty?
    resolved = 0
    values.each do |value|
      target = resolve_name(value, name_lookup)
      if target
        add_relationship!(record, target, relation_type)
        resolved += 1
      end
    end
    if resolved == values.length
      remove_preservation_field!(record, field)
      REPORT[:fields_fully_modeled] << { path: record.path.to_s, field: field }
    elsif resolved.positive?
      REPORT[:fields_partially_modeled] << { path: record.path.to_s, field: field, resolved: resolved, total: values.length }
    end
  end

  record.meta.delete('relationships') if record.meta['relationships'] == []
  dump_record(record)
end

report_path = ROOT + 'docs/development/AETHERHAVEN_CONTENT_SCHEMA_V1_SEMANTIC_AUDIT.md'
lines = [
  '# Aetherhaven Content Schema Version 1 — Semantic Migration Audit', '',
  '**Audit date:** 2026-08-10  ',
  '**Schema:** `1.0.0 — LOCKED`', '',
  'This pass runs after the deterministic legacy-field migration and corrects semantic issues that structural validation alone cannot detect. It uses the pre-migration `main` records only to recover already-existing metadata; it does not generate new canon.', '',
  '## Summary', '',
  "- Additional canonical relationships recovered: **#{REPORT[:relationships_added].length}**",
  "- Legacy fields fully modeled and removed from preservation notes: **#{REPORT[:fields_fully_modeled].length}**",
  "- Legacy fields partially modeled while preserving the original note: **#{REPORT[:fields_partially_modeled].length}**",
  "- Character asset roles corrected from assumed portrait to neutral reference: **#{REPORT[:character_asset_roles_corrected].length}**",
  "- Artifact catalog-number corrections/removals: **#{REPORT[:catalog_numbers_corrected].length}**",
  "- Story chronology states corrected to relative placement: **#{REPORT[:story_chronology_corrected].length}**", '',
  '## Catalog Number Corrections', ''
]
if REPORT[:catalog_numbers_corrected].empty?
  lines << '- None.'
else
  REPORT[:catalog_numbers_corrected].each { |item| lines << "- `#{item[:path]}`: `#{item[:from].to_s.gsub('`', '\\`')}` → `#{item[:to] || '[removed: no exact visible catalog identifier]'}`" }
end
lines += ['', '## Partial Relationship Enrichment', '']
if REPORT[:fields_partially_modeled].empty?
  lines << '- None.'
else
  REPORT[:fields_partially_modeled].each { |item| lines << "- `#{item[:path]}` — `#{item[:field]}`: modeled #{item[:resolved]} of #{item[:total]}; original preservation note retained." }
end
lines += ['', '## Safety Rule', '', 'No unresolved or ambiguous value is promoted to a canonical-ID relationship. Partial or unresolved legacy content remains visible in the owning Markdown preservation notes until separately modeled or resolved.', '']
File.write(report_path, lines.join("\n") + "\n", encoding: 'UTF-8')

puts JSON.pretty_generate(REPORT.transform_values { |value| value.length })
