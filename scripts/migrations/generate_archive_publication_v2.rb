#!/usr/bin/env ruby
# frozen_string_literal: true

require 'yaml'
require 'json'
require 'date'
require 'digest'
require 'pathname'
require 'fileutils'

ROOT = Pathname.new(Dir.pwd).realpath
CANON_ROOTS = %w[characters locations organizations artifacts vessels historical_events story_drafts story_arcs].freeze
PUBLIC_ROOT = ROOT + 'website/content/public'
OLD_MANIFEST = PUBLIC_ROOT + 'manifest.json'
OLD_PRESENTATION = PUBLIC_ROOT + 'archive-presentation.json'
NEW_MANIFEST = PUBLIC_ROOT + 'manifest.v2.json'
NEW_PRESENTATION = PUBLIC_ROOT + 'archive-presentation.v2.json'
REPORT_PATH = ROOT + 'docs/development/AETHERHAVEN_ARCHIVE_PUBLICATION_V2_GENERATION.md'


def normalize_dates(value)
  case value
  when Date, Time, DateTime
    value.strftime('%Y-%m-%d')
  when Hash
    value.to_h { |k, v| [k.to_s, normalize_dates(v)] }
  when Array
    value.map { |v| normalize_dates(v) }
  else
    value
  end
end


def parse_frontmatter(path)
  text = File.read(path, encoding: 'UTF-8')
  match = text.match(/\A---\s*\n(.*?)\n---\s*\n/m)
  raise "#{path}: missing YAML front matter" unless match
  normalize_dates(YAML.safe_load(match[1], permitted_classes: [Date, Time, DateTime], aliases: false) || {})
end


def derive_entity_type(record)
  case record.fetch('record_type')
  when 'character' then 'character'
  when 'location' then record['subtype'] == 'district' ? 'district' : 'location'
  when 'organization' then 'organization'
  when 'artifact' then 'artifact'
  when 'vessel' then 'vessel'
  when 'historical_event' then 'event'
  when 'story' then 'story'
  when 'story_arc' then 'story-arc'
  else raise "Unsupported canonical record type: #{record['record_type']}"
  end
end


def selected_asset(record)
  projection = record['public_projection']
  selection = projection&.dig('image')
  return nil unless selection
  asset = Array(record['assets']).find { |candidate| candidate['id'] == selection['asset'] }
  raise "#{record['id']}: selected asset does not exist: #{selection['asset']}" unless asset
  unless %w[public teaser].include?(asset['visibility'])
    raise "#{record['id']}: selected asset is not public-safe: #{asset['id']}"
  end
  asset
end


def normalized_projection(record)
  projection = record.fetch('public_projection')
  asset = selected_asset(record)
  image = nil
  if asset
    source = (ROOT + asset.fetch('path')).cleanpath
    raise "#{record['id']}: public asset missing: #{asset['path']}" unless source.file?
    image = {
      'assetId' => asset.fetch('id'),
      'alt' => projection.dig('image', 'alt') || asset.fetch('alt'),
      'sourceSha256' => Digest::SHA256.file(source).hexdigest
    }
  end
  {
    'id' => record.fetch('id'),
    'slug' => record.fetch('slug'),
    'entityType' => derive_entity_type(record),
    'canonicalName' => record.fetch('name'),
    'publicTitle' => projection.fetch('title'),
    'publicSummary' => projection.fetch('summary'),
    'spoilerClassification' => projection.fetch('classification'),
    'publicAccessLabel' => projection.fetch('access_label'),
    'archiveSection' => projection.fetch('archive_section'),
    'tags' => Array(projection.fetch('tags')),
    'relatedEntryIds' => Array(projection.fetch('related')),
    'image' => image
  }
end


def hash_projection(record)
  payload = normalized_projection(record)
  "sha256:#{Digest::SHA256.hexdigest(JSON.generate(payload))}"
end

records = []
CANON_ROOTS.each do |root|
  dir = ROOT + root
  next unless dir.directory?
  Dir.glob((dir + '*.md').to_s).sort.each do |absolute|
    next if File.basename(absolute) == 'README.md'
    record = parse_frontmatter(absolute)
    next unless record['schema_version'] == 1
    records << record
  end
end

by_slug = records.to_h { |record| [record.fetch('slug'), record] }
by_id = records.to_h { |record| [record.fetch('id'), record] }
old_manifest = JSON.parse(File.read(OLD_MANIFEST, encoding: 'UTF-8'))
old_presentation = JSON.parse(File.read(OLD_PRESENTATION, encoding: 'UTF-8'))
raise 'Expected publication manifest schemaVersion 1.' unless old_manifest['schemaVersion'] == 1
raise 'Expected presentation manifest schemaVersion 1.' unless old_presentation['schemaVersion'] == 1

old_id_to_canonical = {}
old_manifest.fetch('entries').each do |entry|
  record = by_slug[entry.fetch('slug')]
  raise "No Schema v1 record owns public slug #{entry['slug']}" unless record
  raise "#{record['id']}: missing public_projection" unless record['public_projection']
  old_id_to_canonical[entry.fetch('id')] = record.fetch('id')
end

parity_failures = []
old_manifest.fetch('entries').each do |entry|
  record = by_id.fetch(old_id_to_canonical.fetch(entry.fetch('id')))
  projection = record.fetch('public_projection')
  expected_related = Array(entry['relatedEntryIds']).map { |old_id| old_id_to_canonical.fetch(old_id) }
  comparisons = {
    'canonicalName' => [entry['canonicalName'], record['name']],
    'publicTitle' => [entry['publicTitle'], projection['title']],
    'publicSummary' => [entry['publicSummary'], projection['summary']],
    'spoilerClassification' => [entry['spoilerClassification'], projection['classification']],
    'publicAccessLabel' => [entry['publicAccessLabel'] || entry['spoilerClassification'], projection['access_label']],
    'tags' => [Array(entry['tags']), Array(projection['tags'])],
    'relatedEntryIds' => [expected_related, Array(projection['related'])]
  }
  comparisons.each do |field, (old_value, new_value)|
    parity_failures << "#{entry['id']} #{field} differs" unless old_value == new_value
  end
  expected_section = Array(entry['tags']).include?('hidden-archive') ? 'hidden' : 'catalog'
  parity_failures << "#{entry['id']} archive section differs" unless projection['archive_section'] == expected_section
  if entry['image']
    asset = selected_asset(record)
    parity_failures << "#{entry['id']} image missing from migrated projection" unless asset
    parity_failures << "#{entry['id']} image alt differs" unless projection.dig('image', 'alt') == entry.dig('image', 'alt')
  elsif projection['image']
    parity_failures << "#{entry['id']} gained an unapproved public image"
  end
end
raise "C1 projection parity failed:\n#{parity_failures.join("\n")}" unless parity_failures.empty?

ledger_entries = old_manifest.fetch('entries').map do |entry|
  record = by_id.fetch(old_id_to_canonical.fetch(entry.fetch('id')))
  approval = entry.fetch('approval')
  {
    'id' => record.fetch('id'),
    'projectionHash' => hash_projection(record),
    'approvedBy' => approval.fetch('approvedBy'),
    'approvedOn' => approval.fetch('approvedOn'),
    'publicationDate' => entry['publicationDate'] || approval.fetch('approvedOn')
  }
end

new_manifest = {
  'schemaVersion' => 2,
  'entries' => ledger_entries
}

new_map_entries = old_presentation.fetch('mapEntries').map do |entry|
  {
    'id' => old_id_to_canonical.fetch(entry.fetch('id')),
    **(entry.key?('mapPosition') ? { 'mapPosition' => entry['mapPosition'] } : {}),
    'mapRegion' => entry.fetch('mapRegion'),
    'mapLabel' => entry.fetch('mapLabel')
  }
end

new_route = old_presentation.fetch('curatorRoute').map do |step|
  if step['kind'] == 'room'
    step
  else
    step.merge('id' => old_id_to_canonical.fetch(step.fetch('id')))
  end
end

new_presentation = {
  'schemaVersion' => 2,
  'approval' => old_presentation.fetch('approval'),
  'mapEntries' => new_map_entries,
  'curatorRoute' => new_route
}

File.write(NEW_MANIFEST, JSON.pretty_generate(new_manifest) + "\n", encoding: 'UTF-8')
File.write(NEW_PRESENTATION, JSON.pretty_generate(new_presentation) + "\n", encoding: 'UTF-8')

lines = [
  '# Aetherhaven Archive Publication Version 2 — Generation Report', '',
  '**Generated:** 2026-08-10  ',
  '**Source:** Schema Version 1 canonical Markdown + existing author-approved C1 publication manifests', '',
  '## Result', '',
  "- Canonical Schema v1 records scanned: **#{records.length}**",
  "- Existing approved C1 projections verified against owning Markdown: **#{old_manifest['entries'].length}**",
  "- Version 2 approval-ledger entries generated: **#{ledger_entries.length}**",
  "- Presentation map entries converted to canonical IDs: **#{new_map_entries.length}**",
  "- Curator Route steps preserved: **#{new_route.length}**",
  '- Public titles, summaries, classifications, access labels, tags, public related-record sets, image selections, and image alt text were required to match the existing C1 release exactly before generation.',
  '- Each approval hash includes the canonical ID, stable slug, derived public entity type, canonical name, reader-facing projection, related canonical IDs, selected asset ID/alt, and SHA-256 digest of selected source-image bytes.',
  '- These files are candidates until the Astro loader and production verifier accept them. The existing Version 1 manifests remain active during this checkpoint.', '',
  '## Candidate Files', '',
  '- `website/content/public/manifest.v2.json`',
  '- `website/content/public/archive-presentation.v2.json`', ''
]
FileUtils.mkdir_p(REPORT_PATH.dirname)
File.write(REPORT_PATH, lines.join("\n"), encoding: 'UTF-8')

puts JSON.pretty_generate(
  records: records.length,
  projections: old_manifest['entries'].length,
  ledger_entries: ledger_entries.length,
  map_entries: new_map_entries.length,
  route_steps: new_route.length
)
