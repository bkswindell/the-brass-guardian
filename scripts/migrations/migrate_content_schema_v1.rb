#!/usr/bin/env ruby
# frozen_string_literal: true

require 'yaml'
require 'json'
require 'date'
require 'pathname'
require 'fileutils'

ROOT = Pathname.new(Dir.pwd).realpath
CANON_ROOTS = {
  'characters' => 'character',
  'locations' => 'location',
  'organizations' => 'organization',
  'artifacts' => 'artifact',
  'vessels' => 'vessel',
  'historical_events' => 'historical_event',
  'story_drafts' => 'story',
  'story_arcs' => 'story_arc'
}.freeze

ID_KEYS = {
  'character' => 'character_id',
  'location' => 'location_id',
  'organization' => 'organization_id',
  'artifact' => 'artifact_id',
  'historical_event' => 'historical_event_id',
  'story' => 'story_draft_id',
  'story_arc' => 'story_arc_id',
  'vessel' => 'vessel_id'
}.freeze

RELATION_FIELDS = {
  'character' => {
    'primary_locations' => 'primary-location',
    'affiliations' => 'affiliated-with',
    'key_connections' => 'connected-to',
    'related_markdown' => 'related-to'
  },
  'location' => {
    'parent_location' => 'parent-location',
    'primary_connections' => 'connected-to',
    'points_of_interest' => 'contains',
    'related_markdown' => 'related-to'
  },
  'organization' => {
    'headquarters' => 'headquartered-at',
    'leadership' => 'led-by',
    'governing_authority' => 'governed-by',
    'key_relationships' => 'related-to',
    'related_markdown' => 'related-to'
  },
  'artifact' => {
    'related_markdown' => 'related-to',
    'related_historical_events' => 'related-historical-event'
  },
  'historical_event' => {
    'locations' => 'occurred-at',
    'participants' => 'participant',
    'organizations' => 'involved-organization',
    'related_artifacts' => 'related-artifact',
    'related_story_arcs' => 'related-story-arc',
    'related_markdown' => 'related-to',
    'order_interest' => 'interest-from'
  },
  'story' => {
    'primary_characters' => 'features-character',
    'primary_locations' => 'features-location',
    'primary_organizations' => 'features-organization',
    'primary_artifacts' => 'features-artifact',
    'primary_connections' => 'related-to',
    'related_markdown' => 'related-to'
  },
  'story_arc' => {
    'primary_character' => 'features-character',
    'primary_characters' => 'features-character',
    'primary_protagonist' => 'features-character',
    'primary_protagonists' => 'features-character',
    'primary_locations' => 'features-location',
    'primary_organizations' => 'features-organization',
    'primary_artifacts' => 'features-artifact',
    'related_story_drafts' => 'related-story',
    'related_markdown' => 'related-to'
  },
  'vessel' => {
    'primary_connections' => 'connected-to',
    'related_markdown' => 'related-to'
  }
}.freeze

GLOBAL_CONSUMED = %w[
  series canon_status canonical_scope last_updated temporal_relevance aliases name title type
  source_basis source source_scope canonical_images artwork date_status chronology spoiler_level
  slug schema_version id record_type canon development disclosure descriptor subtype provenance
  relationships assets cartography public_projection character location organization artifact
  historical_event story vessel production
].freeze

TYPE_CONSUMED = {
  'character' => %w[title age_status public_identity former_role former_roles current_role current_roles],
  'location' => %w[jurisdiction access_status map_reference_category map_number parent_location primary_connections points_of_interest],
  'organization' => %w[primary_jurisdiction headquarters leadership governing_authority key_relationships access_classes],
  'artifact' => %w[category catalog_number slate_number image_status visual_transcription_status],
  'historical_event' => %w[public_record_status restricted_record_status order_interest locations participants organizations related_artifacts related_story_arcs],
  'story' => %w[subtitle title_status proposed_book proposed_placement primary_characters primary_locations primary_organizations primary_artifacts primary_connections],
  'story_arc' => %w[primary_character primary_characters primary_protagonist primary_protagonists primary_locations primary_organizations primary_artifacts related_story_drafts],
  'vessel' => %w[class status primary_connections]
}.freeze

PUBLIC_IMAGE_SOURCE_HINTS = {
  /map-of-aetherhaven/i => 'art/Map_of_Aetherhaven.png',
  /clockwork-gardens-at-night/i => 'art/Clockwork_Gardens_at_Night.png',
  /wayfinder-above-clouds/i => 'art/Wayfinder_Above_the_Clouds.png'
}.freeze

Record = Struct.new(
  :path, :record_type, :legacy_meta, :body, :id, :name, :aliases, :slug,
  :public_entry, :new_meta, :special, keyword_init: true
)

REPORT = {
  migrated: [],
  already_v1: [],
  created: [],
  unresolved_relationship_values: [],
  preserved_unknown_legacy_fields: [],
  skipped_missing_assets: [],
  scope_fallbacks: [],
  slug_adjustments: [],
  public_projections: [],
  warnings: []
}

def deep_stringify_dates(value)
  case value
  when Date, Time, DateTime
    value.strftime('%Y-%m-%d')
  when Hash
    value.to_h { |k, v| [k.to_s, deep_stringify_dates(v)] }
  when Array
    value.map { |v| deep_stringify_dates(v) }
  else
    value
  end
end

def parse_markdown(path)
  text = File.read(path, encoding: 'UTF-8')
  match = text.match(/\A---\s*\n(.*?)\n---\s*\n(.*)\z/m)
  raise "#{path}: missing YAML front matter" unless match
  raw = YAML.safe_load(match[1], permitted_classes: [Date, Time, DateTime], aliases: false) || {}
  [deep_stringify_dates(raw), match[2]]
end

def dump_markdown(meta, body)
  yaml = YAML.dump(meta, line_width: -1).sub(/\A---\s*\n/, '')
  "---\n#{yaml}---\n#{body}"
end

def blankish?(value)
  value.nil? || value == '' || value == [] || value == {} ||
    (value.is_a?(Array) && value.all? { |v| blankish?(v) })
end

def listify(value)
  return [] if blankish?(value)
  value.is_a?(Array) ? value.compact : [value]
end

def slugify(value)
  value.to_s.downcase.gsub(/[’'`]/, '').gsub(/&/, ' and ').gsub(/[^a-z0-9]+/, '-').gsub(/\A-+|-+\z/, '').gsub(/-+/, '-')
end

def normalize_name(value)
  value.to_s.downcase.gsub(/[“”]/, '"').gsub(/[’'`]/, '').gsub(/&/, ' and ').gsub(/[^a-z0-9]+/, ' ').strip.gsub(/\s+/, ' ')
end

def normalize_scope(value)
  listify(value).map { |v| slugify(v) }.reject(&:empty?).uniq
end

def normalize_temporal_relevance(value)
  return nil if blankish?(value)
  key = slugify(value)
  case key
  when 'very-high', 'veryhigh' then 'very-high'
  when 'none', 'low', 'moderate', 'high', 'critical', 'unresolved' then key
  else nil
  end
end

def canonical_status(meta, record_type)
  text = [meta['canon_status'], meta['image_status']].compact.join(' ').downcase
  return 'superseded' if text.include?('supersed')
  return 'proposed' if text.include?('requires-canon-review')
  return 'proposed' if text.include?('planned-artifact-concept')
  return 'proposed' if record_type == 'artifact' && text.match?(/\bdraft\b/) && !text.include?('canonical')
  return 'proposed' if text.strip == 'draft'
  'canonical'
end

def development_status(meta, canon_status_value)
  text = [meta['canon_status'], meta['image_status']].compact.join(' ').downcase
  return 'placeholder' if text.include?('placeholder')
  return 'concept' if canon_status_value == 'proposed' || text.include?('concept') || text.include?('planned')
  return 'complete' if text.include?('complete') || text.include?('final')
  'working'
end

def disclosure_level(record, canon_status_value)
  meta = record.legacy_meta || {}
  text = [meta['canon_status'], meta['spoiler_level'], meta['type'], meta['title_status']].compact.join(' ').downcase
  return 'creator-only' if canon_status_value == 'proposed'
  return 'creator-only' if record.record_type == 'story_arc'
  return 'creator-only' if text.match?(/ultimate|major long-range|major spoiler|concealed role|long-range|future story|delayed-reveal/)
  return 'creator-only' if record.path.to_s.include?('Hidden_Architect') || record.path.to_s.include?('Silas_Rook')
  return 'story-sensitive' if text.match?(/hidden|restricted|spoiler/)
  return 'story-sensitive' if %w[story historical_event artifact].include?(record.record_type)
  'story-sensitive'
end

def source_kind(ref)
  text = ref.to_s.downcase
  return 'manuscript' if text.end_with?('.pdf', '.docx') || text.include?('manuscript')
  return 'canonical-record' if text.end_with?('.md') || text.include?('canonical markdown')
  return 'author-decision' if text.include?('decision') || text.include?('approved') || text.include?('canon decisions')
  return 'artwork' if text.match?(/\.(png|jpe?g|webp|svg)$/)
  'external'
end

def provenance_from(meta)
  sources = []
  listify(meta['source_basis']).each do |ref|
    next if blankish?(ref)
    sources << { 'kind' => source_kind(ref), 'ref' => ref.to_s }
  end
  unless blankish?(meta['source'])
    src = { 'kind' => source_kind(meta['source']), 'ref' => meta['source'].to_s }
    src['note'] = meta['source_scope'].to_s unless blankish?(meta['source_scope'])
    sources << src
  end
  sources.uniq { |s| [s['kind'], s['ref'], s['note']] }
end

def repo_relative_asset(ref, record_path)
  return nil if blankish?(ref)
  raw = ref.to_s.strip
  return nil if raw.empty? || raw == 'null'
  candidate = if raw.start_with?('../', './')
                (ROOT + record_path.dirname + raw).cleanpath
              elsif raw.start_with?('art/')
                ROOT + raw
              else
                direct = ROOT + raw
                File.exist?(direct) ? direct : (ROOT + record_path.dirname + raw).cleanpath
              end
  begin
    relative = Pathname.new(candidate).relative_path_from(ROOT).to_s
  rescue ArgumentError
    return nil
  end
  return nil if relative.split('/').include?('..') || relative.split('/').include?('unused')
  return nil unless relative.start_with?('art/')
  relative
end

def asset_role(record_type, path, index, explicit = nil)
  return explicit if explicit
  base = File.basename(path).downcase
  return 'map' if base.include?('map')
  return 'plate' if record_type == 'artifact'
  return 'portrait' if record_type == 'character' && index.zero?
  return 'cover' if record_type == 'story' && base.include?('cover')
  'reference'
end

def asset_alt(record, role)
  case role
  when 'portrait' then "Canonical visual reference portrait for #{record.name}."
  when 'map' then "Canonical map reference associated with #{record.name}."
  when 'plate' then "Canonical archival plate for #{record.name}."
  when 'cover' then "Canonical cover illustration for #{record.name}."
  else "Canonical visual reference for #{record.name}."
  end
end

def status_visibility(record)
  level = record.new_meta&.dig('disclosure', 'level') || 'story-sensitive'
  level == 'creator-only' ? 'creator-only' : 'story-sensitive'
end

def extract_assets(record)
  meta = record.legacy_meta || {}
  assets = []
  listify(meta['canonical_images']).each_with_index do |raw, index|
    path = repo_relative_asset(raw, record.path)
    unless path && File.file?(ROOT + path)
      REPORT[:skipped_missing_assets] << { path: record.path.to_s, value: raw.to_s } unless blankish?(raw)
      next
    end
    role = asset_role(record.record_type, path, index)
    assets << { 'id' => slugify("#{role}-#{index + 1}"), 'path' => path, 'role' => role, 'visibility' => status_visibility(record), 'alt' => asset_alt(record, role) }
  end
  artwork = meta['artwork']
  if artwork.is_a?(Hash)
    unless blankish?(artwork['cover_image'])
      path = repo_relative_asset(artwork['cover_image'], record.path)
      if path && File.file?(ROOT + path)
        assets << { 'id' => 'cover', 'path' => path, 'role' => 'cover', 'visibility' => status_visibility(record), 'alt' => asset_alt(record, 'cover') }
      else
        REPORT[:skipped_missing_assets] << { path: record.path.to_s, value: artwork['cover_image'].to_s }
      end
    end
    listify(artwork['inline_images']).each_with_index do |entry, index|
      next unless entry.is_a?(Hash) && !blankish?(entry['file'])
      path = repo_relative_asset(entry['file'], record.path)
      unless path && File.file?(ROOT + path)
        REPORT[:skipped_missing_assets] << { path: record.path.to_s, value: entry['file'].to_s }
        next
      end
      asset = { 'id' => "inline-#{index + 1}", 'path' => path, 'role' => 'inline', 'visibility' => status_visibility(record), 'alt' => asset_alt(record, 'reference') }
      asset['placement'] = entry['placement'].to_s unless blankish?(entry['placement'])
      assets << asset
    end
  end
  seen = {}
  assets.select do |asset|
    key = [asset['path'], asset['role'], asset['placement']]
    next false if seen[key]
    seen[key] = true
  end
end

def public_source_asset(image_src, record)
  return nil if blankish?(image_src)
  PUBLIC_IMAGE_SOURCE_HINTS.each { |pattern, source| return source if image_src.match?(pattern) && File.file?(ROOT + source) }
  assets = record.new_meta['assets'] || []
  return assets.first['path'] if assets.length == 1
  nil
end

def chronology_from(meta, record_type)
  raw = meta['chronology']
  return nil if blankish?(raw)
  values = listify(raw).map { |value| value.is_a?(Hash) ? value.to_json : value.to_s }.reject(&:empty?)
  return nil if values.empty?
  display = values.join('; ')
  date_status = meta['date_status'].to_s
  combined = "#{date_status} #{display}".downcase
  status = if combined.match?(/disput|contradict|conflict/)
             'disputed'
           elsif combined.match?(/anomal|temporal|impossible|out of sequence|out-of-sequence/)
             'anomalous'
           elsif date_status.downcase.include?('exact') && !date_status.downcase.include?('unresolved')
             'exact'
           elsif combined.match?(/approxim|circa/)
             'approximate'
           elsif combined.match?(/\bbetween\b|\brange\b/)
             'range'
           elsif combined.match?(/before|after|present-day|present day|volume|opening story|first chapter/)
             'relative'
           elsif combined.match?(/unresolved|unknown/)
             'unknown'
           elsif record_type == 'story'
             'relative'
           else
             'unknown'
           end
  result = { 'status' => status, 'display' => display }
  result['note'] = date_status unless date_status.empty? || display.downcase.include?(date_status.downcase)
  result
end

def extract_catalog_number(body)
  [/CATALOG\s+No\.?\s*[:`]*\s*([A-Z]{1,5}-\d+-\d{3})/i, /CATALOG\s+No\.?[^\n]*`([^`]+)`/i].each do |pattern|
    match = body.match(pattern)
    return match[1].strip if match
  end
  nil
end

def path_from_ref(ref, from_path)
  raw = ref.to_s.strip
  link = raw.match(/\[[^\]]+\]\(([^)]+)\)/)
  raw = link[1] if link
  raw = raw.split('#', 2).first
  return nil if raw.empty?
  candidate = if raw.start_with?('../', './')
                (ROOT + from_path.dirname + raw).cleanpath
              else
                direct = ROOT + raw
                File.exist?(direct) ? direct : (ROOT + from_path.dirname + raw).cleanpath
              end
  begin
    Pathname.new(candidate).relative_path_from(ROOT).to_s
  rescue ArgumentError
    nil
  end
end

def build_name_lookup(records)
  lookup = Hash.new { |h, k| h[k] = [] }
  records.each do |record|
    [record.name, *record.aliases, record.path.basename('.md').to_s.tr('_', ' ')].each do |value|
      key = normalize_name(value)
      next if key.empty?
      lookup[key] << record.id unless lookup[key].include?(record.id)
      if key.start_with?('the ')
        short = key.sub(/\Athe\s+/, '')
        lookup[short] << record.id unless lookup[short].include?(record.id)
      end
    end
  end
  lookup
end

def resolve_target(value, record, path_lookup, name_lookup)
  return [nil, 'blank'] if blankish?(value)
  return [nil, 'structured value'] if value.is_a?(Hash) || value.is_a?(Array)
  raw = value.to_s.strip
  linked = raw.match(/\[([^\]]+)\]\(([^)]+)\)/)
  if linked
    path = path_from_ref(linked[2], record.path)
    return [path_lookup[path], nil] if path && path_lookup[path]
    raw = linked[1]
  end
  if raw.end_with?('.md') || raw.include?('../') || raw.include?('/')
    path = path_from_ref(raw, record.path)
    return [path_lookup[path], nil] if path && path_lookup[path]
  end
  candidates = [raw]
  candidates << raw.split(',', 2).first if raw.include?(',')
  candidates << raw.gsub(/\s*\([^)]*\)\s*/, ' ').strip if raw.include?('(')
  candidates.uniq.each do |candidate|
    ids = name_lookup[normalize_name(candidate)]
    return [ids.first, nil] if ids&.length == 1
  end
  [nil, 'no unique canonical target']
end

def relation_visibility_from_public(source_entry, target_entry)
  return 'teaser' if source_entry['spoilerClassification'] == 'teaser' || target_entry['spoilerClassification'] == 'teaser'
  'public'
end

def add_relationship!(relationships, target, type, visibility, note = nil)
  return if target.nil?
  existing = relationships.find { |r| r['target'] == target && r['type'] == type }
  if existing
    existing['visibility'] = visibility if %w[public teaser].include?(visibility) && !%w[public teaser].include?(existing['visibility'])
    return existing
  end
  relationship = { 'target' => target, 'type' => type, 'visibility' => visibility }
  relationship['note'] = note unless blankish?(note)
  relationships << relationship
  relationship
end

def public_manifest
  JSON.parse(File.read(ROOT + 'website/content/public/manifest.json', encoding: 'UTF-8'))
end

def discover_records
  records = []
  CANON_ROOTS.each do |dir, record_type|
    root = ROOT + dir
    next unless root.directory?
    Dir.glob((root + '*.md').to_s).sort.each do |absolute|
      next if File.basename(absolute) == 'README.md'
      path = Pathname.new(absolute).relative_path_from(ROOT)
      meta, body = parse_markdown(absolute)
      if meta['schema_version'] == 1
        records << Record.new(path: path, record_type: meta['record_type'] || record_type, legacy_meta: meta, body: body, id: meta['id'], name: meta['name'], aliases: listify(meta['aliases']), slug: meta['slug'], new_meta: meta, special: false)
        REPORT[:already_v1] << path.to_s
        next
      end
      id_key = ID_KEYS.fetch(record_type)
      id = meta[id_key]
      raise "#{path}: missing legacy #{id_key}" if blankish?(id)
      name = meta['name'] || meta['title']
      raise "#{path}: missing canonical name/title" if blankish?(name)
      records << Record.new(path: path, record_type: record_type, legacy_meta: meta, body: body, id: id.to_s, name: name.to_s, aliases: listify(meta['aliases']).map(&:to_s), special: false)
    end
  end
  records
end

def wayfinder_body
  <<~MD
    # The Wayfinder

    > **Canonical vessel profile.** This record owns the *Wayfinder* as a first-class vessel. The technical plate remains authoritative for the plate and visible technical evidence; location records remain authoritative for individual berths and facilities.

    ## Canonical Summary

    The *Wayfinder* is [Professor Elias Hawthorne](../characters/Professor_Elias_Hawthorne.md) and [Amelia Hawthorne](../characters/Amelia_Hawthorne.md)'s exploration airship: part vessel, part workshop, and part home above the clouds.

    She is frequently moored at [the Gardens Airship Landing](../locations/The_Gardens_Airship_Landing.md), where expedition equipment, repairs, and questions collect between journeys. Her hull shows the care of many voyages, and her systems combine practical engineering with older mechanisms that do not surrender their secrets easily.

    The Hawthornes trust the *Wayfinder* not merely as a machine, but as a companion and home.

    ## Visual Reference

    ![The Wayfinder above the clouds](../art/Wayfinder_Above_the_Clouds.png)

    ## Relationships

    - [Professor Elias Hawthorne](../characters/Professor_Elias_Hawthorne.md) — explorer, engineer, and keeper of the vessel.
    - [Amelia Hawthorne](../characters/Amelia_Hawthorne.md) — explorer, mechanic, and resident aboard the vessel.
    - [The Gardens Airship Landing](../locations/The_Gardens_Airship_Landing.md) — familiar home berth between expeditions.
    - [The Wayfinder Technical Plate](../artifacts/007_The_Wayfinder_Technical_Plate.md) — authoritative artifact record for the existing technical plate.

    ## Continuity Notes

    - This profile consolidates already-approved Wayfinder canon; it does not establish new specifications.
    - The vessel is both transportation and a lived-in Hawthorne home.
    - Older or unexplained mechanisms aboard the vessel should remain unexplained unless separately established.
    - Technical artifact details belong in the linked artifact record rather than being duplicated here.

    ## Development Checklist

    - [x] First-class vessel record established by Schema Version 1 migration.
    - [x] Existing public projection preserved.
    - [x] Existing canonical visual reference linked.
    - [ ] Expand technical and operational details only as canon establishes them.
  MD
end

def ensure_wayfinder_record!(records)
  existing = records.find { |r| r.record_type == 'vessel' && normalize_name(r.name) == 'the wayfinder' }
  return existing if existing
  synthetic = {
    'vessel_id' => 'AH-VESSEL-WAYFINDER', 'name' => 'The Wayfinder', 'aliases' => ['Wayfinder'],
    'canon_status' => 'Canonical working profile', 'canonical_scope' => 'Aetherhaven volumes', 'last_updated' => '2026-08-10',
    'primary_connections' => ['Professor Elias Hawthorne', 'Amelia Hawthorne', 'The Gardens Airship Landing', 'The Wayfinder Technical Plate'],
    'canonical_images' => ['../art/Wayfinder_Above_the_Clouds.png'],
    'source_basis' => ['artifacts/007_The_Wayfinder_Technical_Plate.md', 'locations/The_Gardens_Airship_Landing.md', 'story_drafts/The_Brass_Guardian_and_the_Clockwork_Explorer.md'],
    'class' => 'explorer-airship', 'status' => 'active'
  }
  record = Record.new(path: Pathname.new('vessels/The_Wayfinder.md'), record_type: 'vessel', legacy_meta: synthetic, body: wayfinder_body, id: 'AH-VESSEL-WAYFINDER', name: 'The Wayfinder', aliases: ['Wayfinder'], special: true)
  records << record
  record
end

def assign_public_entries!(records, manifest)
  path_lookup = records.to_h { |r| [r.path.to_s, r] }
  manifest.fetch('entries').each do |entry|
    owner = if entry['id'] == 'vessel-wayfinder'
              records.find { |r| r.id == 'AH-VESSEL-WAYFINDER' }
            else
              listify(entry['sourcePaths']).map { |p| path_lookup[p.to_s] }.compact.first
            end
    raise "Public manifest entry #{entry['id']} has no canonical owner" unless owner
    raise "#{owner.path}: multiple public manifest entries map to one canonical record" if owner.public_entry
    owner.public_entry = entry
    owner.name = entry['canonicalName'].to_s unless blankish?(entry['canonicalName'])
  end
end

def assign_slugs!(records)
  used = {}
  records.sort_by { |r| r.path.to_s }.each do |record|
    if record.public_entry
      slug = record.public_entry.fetch('slug')
      raise "duplicate approved public slug: #{slug}" if used[slug]
      record.slug = slug
      used[slug] = record.id
      next
    end
    base = slugify(record.name)
    base = slugify(record.path.basename('.md').to_s) if base.empty?
    candidate = base
    if used[candidate]
      type_suffix = record.record_type.tr('_', '-')
      candidate = "#{base}-#{type_suffix}"
      counter = 2
      while used[candidate]
        candidate = "#{base}-#{type_suffix}-#{counter}"
        counter += 1
      end
      REPORT[:slug_adjustments] << { path: record.path.to_s, from: base, to: candidate }
    end
    record.slug = candidate
    used[candidate] = record.id
  end
end

def migration_notes_body(body, notes)
  return body if notes.empty?
  marker = '## Schema Migration Preservation Notes'
  return body if body.include?(marker)
  lines = ['', '', marker, '', '> These values were preserved verbatim from pre-Version-1 front matter because the migration could not safely convert them into a canonical-ID field without inventing or resolving canon.', '']
  notes.each do |note|
    rendered = note[:value].is_a?(String) ? note[:value] : JSON.generate(note[:value])
    lines << "- **#{note[:field]}:** `#{rendered.gsub('`', '\\`')}`"
  end
  body.rstrip + lines.join("\n") + "\n"
end

def transform_record!(record, _records, path_lookup, name_lookup, public_id_to_canonical, manifest_by_public_id)
  return if record.new_meta && record.new_meta['schema_version'] == 1 && !record.special
  meta = record.legacy_meta || {}
  c_status = canonical_status(meta, record.record_type)
  scope = normalize_scope(meta['canonical_scope'])
  if scope.empty? && c_status != 'proposed'
    scope = ['aetherhaven-volumes']
    REPORT[:scope_fallbacks] << record.path.to_s
  end
  new_meta = {}
  new_meta['schema_version'] = 1
  new_meta['id'] = record.id
  new_meta['record_type'] = record.record_type
  new_meta['name'] = record.name
  new_meta['slug'] = record.slug
  new_meta['aliases'] = record.aliases.uniq
  new_meta['last_updated'] = (meta['last_updated'] || '2026-08-10').to_s
  new_meta['canon'] = { 'status' => c_status, 'scope' => scope }
  dev = { 'status' => development_status(meta, c_status) }
  temporal = normalize_temporal_relevance(meta['temporal_relevance'])
  dev['temporal_relevance'] = temporal if temporal
  new_meta['development'] = dev
  new_meta['disclosure'] = { 'level' => disclosure_level(record, c_status) }
  descriptor = meta['type'].to_s.strip
  new_meta['descriptor'] = descriptor unless descriptor.empty? || descriptor.downcase.include?('placeholder')
  new_meta['subtype'] = 'district' if record.record_type == 'location' && (record.public_entry&.dig('entityType') == 'district' || record.name.downcase.end_with?(' district'))
  provenance = provenance_from(meta)
  new_meta['provenance'] = { 'sources' => provenance } unless provenance.empty?
  record.new_meta = new_meta
  assets = extract_assets(record)
  new_meta['assets'] = assets unless assets.empty?
  if record.record_type == 'location'
    category = meta['map_reference_category'].to_s.strip.downcase
    number = meta['map_number']
    if %w[numbered restricted unlisted].include?(category)
      entry = { 'map_id' => 'aetherhaven-city', 'category' => category }
      entry['reference'] = number.to_s unless category == 'unlisted' || blankish?(number)
      if category != 'unlisted' && blankish?(number)
        REPORT[:warnings] << "#{record.path}: #{category} cartography missing reference; cartography omitted"
      else
        new_meta['cartography'] = [entry]
      end
    end
  end
  chronology = chronology_from(meta, record.record_type)
  new_meta['chronology'] = chronology if chronology
  case record.record_type
  when 'character'
    extension = {}
    titles = listify(meta['title']).map(&:to_s).reject(&:empty?)
    extension['titles'] = titles unless titles.empty?
    extension['age_status'] = meta['age_status'].to_s unless blankish?(meta['age_status'])
    extension['public_identity'] = meta['public_identity'].to_s unless blankish?(meta['public_identity'])
    former = listify(meta['former_roles'] || meta['former_role']).map(&:to_s)
    current = listify(meta['current_roles'] || meta['current_role']).map(&:to_s)
    extension['former_roles'] = former unless former.empty?
    extension['current_roles'] = current unless current.empty?
    new_meta['character'] = extension unless extension.empty?
  when 'location'
    extension = {}
    jurisdiction = listify(meta['jurisdiction']).map(&:to_s).reject(&:empty?)
    access = listify(meta['access_status']).map(&:to_s).reject(&:empty?)
    extension['jurisdiction'] = jurisdiction unless jurisdiction.empty?
    extension['access_status'] = access unless access.empty?
    new_meta['location'] = extension unless extension.empty?
  when 'organization'
    extension = {}
    jurisdiction = listify(meta['primary_jurisdiction']).map(&:to_s).reject(&:empty?)
    extension['jurisdiction'] = jurisdiction unless jurisdiction.empty?
    if record.name == 'The Aetherhaven Archives'
      extension['access_classes'] = ['Open Archives', 'Scholarly Archives', 'Restricted Archives', 'Hidden Archives', 'Lost Archives']
    elsif !blankish?(meta['access_classes'])
      extension['access_classes'] = listify(meta['access_classes']).map(&:to_s)
    end
    new_meta['organization'] = extension unless extension.empty?
  when 'artifact'
    extension = {}
    extension['category'] = meta['category'].to_s unless blankish?(meta['category'])
    catalog = meta['catalog_number'] || extract_catalog_number(record.body)
    extension['catalog_number'] = catalog.to_s unless blankish?(catalog)
    new_meta['artifact'] = extension unless extension.empty?
    production = {}
    production['slate_number'] = Integer(meta['slate_number']) if meta['slate_number'].is_a?(Integer) || meta['slate_number'].to_s.match?(/\A\d+\z/)
    production['image_status'] = meta['image_status'].to_s unless blankish?(meta['image_status'])
    production['visual_transcription_status'] = meta['visual_transcription_status'].to_s unless blankish?(meta['visual_transcription_status'])
    new_meta['production'] = production unless production.empty?
  when 'historical_event'
    extension = {}
    extension['public_record_status'] = meta['public_record_status'].to_s unless blankish?(meta['public_record_status'])
    extension['restricted_record_status'] = meta['restricted_record_status'].to_s unless blankish?(meta['restricted_record_status'])
    new_meta['historical_event'] = extension unless extension.empty?
  when 'story'
    extension = {}
    %w[subtitle title_status proposed_book].each { |field| extension[field] = meta[field].to_s unless blankish?(meta[field]) }
    placement = listify(meta['proposed_placement']).map(&:to_s).reject(&:empty?)
    extension['proposed_placement'] = placement unless placement.empty?
    new_meta['story'] = extension unless extension.empty?
  when 'vessel'
    extension = {}
    extension['class'] = slugify(meta['class']) unless blankish?(meta['class'])
    extension['status'] = slugify(meta['status']) unless blankish?(meta['status'])
    new_meta['vessel'] = extension unless extension.empty?
  end
  unresolved_notes = []
  relationships = []
  (RELATION_FIELDS[record.record_type] || {}).each do |field, relation_type|
    listify(meta[field]).each do |value|
      target, reason = resolve_target(value, record, path_lookup, name_lookup)
      if target && target != record.id
        add_relationship!(relationships, target, relation_type, 'story-sensitive')
      elsif !blankish?(value)
        unresolved_notes << { field: field, value: value }
        REPORT[:unresolved_relationship_values] << { path: record.path.to_s, field: field, value: value, reason: reason }
      end
    end
  end
  entry = record.public_entry
  if entry
    related = listify(entry['relatedEntryIds']).map do |public_id|
      target = public_id_to_canonical[public_id]
      raise "#{record.path}: public related ID #{public_id} has no canonical mapping" unless target
      target_entry = manifest_by_public_id.fetch(public_id)
      safe_visibility = relation_visibility_from_public(entry, target_entry)
      existing = relationships.find { |r| r['target'] == target }
      if existing
        existing['visibility'] = safe_visibility
      else
        add_relationship!(relationships, target, 'public-related', safe_visibility)
      end
      target
    end
    projection = {
      'title' => entry.fetch('publicTitle'), 'summary' => entry.fetch('publicSummary'), 'classification' => entry.fetch('spoilerClassification'),
      'archive_section' => listify(entry['tags']).include?('hidden-archive') ? 'hidden' : 'catalog',
      'access_label' => (entry['publicAccessLabel'] || entry.fetch('spoilerClassification')),
      'tags' => listify(entry['tags']).map(&:to_s), 'related' => related
    }
    if entry['image'].is_a?(Hash)
      source = public_source_asset(entry['image']['src'], record)
      raise "#{record.path}: cannot resolve source asset for public image #{entry['image']['src']}" unless source
      assets = new_meta['assets'] ||= []
      asset = assets.find { |a| a['path'] == source }
      unless asset
        asset = { 'id' => 'public-image', 'path' => source, 'role' => asset_role(record.record_type, source, 0), 'visibility' => entry['spoilerClassification'], 'alt' => entry['image']['alt'] }
        assets << asset
      end
      asset['visibility'] = entry['spoilerClassification']
      asset['alt'] = entry['image']['alt']
      projection['image'] = { 'asset' => asset['id'], 'alt' => entry['image']['alt'] }
    end
    new_meta['public_projection'] = projection
    REPORT[:public_projections] << { path: record.path.to_s, public_id: entry['id'], canonical_id: record.id }
  end
  new_meta['relationships'] = relationships unless relationships.empty?
  consumed = GLOBAL_CONSUMED + TYPE_CONSUMED.fetch(record.record_type, []) + (RELATION_FIELDS[record.record_type] || {}).keys + [ID_KEYS[record.record_type]]
  meta.each do |key, value|
    next if consumed.include?(key) || blankish?(value)
    unresolved_notes << { field: key, value: value }
    REPORT[:preserved_unknown_legacy_fields] << { path: record.path.to_s, field: key, value: value }
  end
  record.body = migration_notes_body(record.body, unresolved_notes)
  record.new_meta = new_meta
end

def validate_asset_paths!(records)
  records.each do |record|
    listify(record.new_meta['assets']).each do |asset|
      path = asset['path'].to_s
      absolute = (ROOT + path).cleanpath
      raise "#{record.path}: unsafe asset path #{path}" unless absolute.to_s.start_with?(ROOT.to_s + File::SEPARATOR)
      raise "#{record.path}: asset path under unused/: #{path}" if path.split('/').include?('unused')
      raise "#{record.path}: asset file missing: #{path}" unless File.file?(absolute)
    end
  end
end

def validate_cross_record!(records)
  ids = {}
  slugs = {}
  records.each do |record|
    raise "duplicate canonical ID #{record.id}" if ids[record.id]
    raise "duplicate canonical slug #{record.slug}" if slugs[record.slug]
    ids[record.id] = record
    slugs[record.slug] = record
  end
  records.each do |record|
    listify(record.new_meta['relationships']).each { |relationship| raise "#{record.path}: unknown relationship target #{relationship['target']}" unless ids[relationship['target']] }
    listify(record.new_meta.dig('public_projection', 'related')).each do |target|
      raise "#{record.path}: unknown public relationship target #{target}" unless ids[target]
      safe = listify(record.new_meta['relationships']).find { |relationship| relationship['target'] == target && %w[public teaser].include?(relationship['visibility']) }
      raise "#{record.path}: public relation #{target} lacks public/teaser relationship" unless safe
    end
  end
end

def write_records!(records)
  records.each do |record|
    absolute = ROOT + record.path
    next if record.new_meta['schema_version'] == 1 && REPORT[:already_v1].include?(record.path.to_s) && !record.special
    FileUtils.mkdir_p(absolute.dirname)
    File.write(absolute, dump_markdown(record.new_meta, record.body), mode: 'w', encoding: 'UTF-8')
    record.special ? REPORT[:created] << record.path.to_s : REPORT[:migrated] << record.path.to_s
  end
end

def export_metadata!(records)
  File.write(ROOT + 'website/.canon-schema-v1-migration-records.json', JSON.pretty_generate(records.map(&:new_meta)) + "\n", encoding: 'UTF-8')
end

def write_report!(records)
  path = ROOT + 'docs/development/AETHERHAVEN_CONTENT_SCHEMA_V1_MIGRATION_REPORT.md'
  lines = ['# Aetherhaven Content Schema Version 1 — Migration Report', '', '**Migration date:** 2026-08-10  ', '**Schema:** `1.0.0 — LOCKED`  ', '**Branch:** `migration/content-schema-v1`', '', '## Summary', '']
  lines << "- Schema-governed records discovered: **#{records.length}**"
  lines << "- Legacy records migrated: **#{REPORT[:migrated].length}**"
  lines << "- First-class records created: **#{REPORT[:created].length}**"
  lines << "- Existing Version 1 records encountered: **#{REPORT[:already_v1].length}**"
  lines << "- Current C1 public projections copied into owning Markdown: **#{REPORT[:public_projections].length}**"
  lines << "- Unresolved relationship-like legacy values preserved in prose: **#{REPORT[:unresolved_relationship_values].length}**"
  lines << "- Other legacy fields preserved in prose: **#{REPORT[:preserved_unknown_legacy_fields].length}**"
  lines << "- Missing/invalid legacy asset references skipped: **#{REPORT[:skipped_missing_assets].length}**"
  lines += ['', 'The migration rewrote front matter only, except when a legacy structured value could not be converted safely. Such values were appended verbatim under `Schema Migration Preservation Notes` in the owning Markdown record rather than being discarded or interpreted.', '', '## Public Projection Preservation', '', 'The exact current C1 `publicTitle`, `publicSummary`, classification, access label, tags, related-record set, slug, and selected image context were copied from the approved Version 1 website manifest into each owning canonical record as `public_projection`. Publication approval remains in the existing website manifest until the later Version 2 ledger cutover.', '', '## Created First-Class Records', '']
  REPORT[:created].each { |value| lines << "- `#{value}`" }
  lines += ['', '## Slug Adjustments for Non-Public Records', '']
  REPORT[:slug_adjustments].empty? ? lines << '- None.' : REPORT[:slug_adjustments].each { |item| lines << "- `#{item[:path]}`: `#{item[:from]}` → `#{item[:to]}`" }
  lines += ['', '## Preserved Unresolved Legacy Relationship Values', '']
  REPORT[:unresolved_relationship_values].empty? ? lines << '- None.' : REPORT[:unresolved_relationship_values].each { |item| lines << "- `#{item[:path]}` — `#{item[:field]}`: `#{item[:value].to_s.gsub('`', '\\`')}`" }
  lines += ['', '## Other Preserved Legacy Fields', '']
  if REPORT[:preserved_unknown_legacy_fields].empty?
    lines << '- None.'
  else
    REPORT[:preserved_unknown_legacy_fields].each do |item|
      rendered = item[:value].is_a?(String) ? item[:value] : JSON.generate(item[:value])
      lines << "- `#{item[:path]}` — `#{item[:field]}`: `#{rendered.gsub('`', '\\`')}`"
    end
  end
  lines += ['', '## Skipped Legacy Asset References', '']
  REPORT[:skipped_missing_assets].empty? ? lines << '- None.' : REPORT[:skipped_missing_assets].each { |item| lines << "- `#{item[:path]}`: `#{item[:value]}`" }
  lines += ['', '## Scope Fallbacks', '']
  if REPORT[:scope_fallbacks].empty?
    lines << '- None.'
  else
    lines << 'The following active canonical records lacked an explicit legacy canonical scope and were assigned the repository-wide Aetherhaven scope `aetherhaven-volumes` without changing story content:'
    REPORT[:scope_fallbacks].each { |value| lines << "- `#{value}`" }
  end
  lines += ['', '## Validation State', '', '- Ruby migration checks require unique IDs/slugs, resolved relationship targets, safe public relationships, and existing active asset files.', '- The workflow exports every migrated metadata object and runs the repository’s locked JavaScript `validateCanonRecords()` implementation over the complete set.', '- Website publication/Preview parity is **not** cut over in this migration; the existing C1 website data sources remain active until the later source-of-truth realignment passes the explicit C1 parity gate.', '']
  FileUtils.mkdir_p(path.dirname)
  File.write(path, lines.join("\n") + "\n", encoding: 'UTF-8')
end

records = discover_records
ensure_wayfinder_record!(records)
manifest = public_manifest
assign_public_entries!(records, manifest)
assign_slugs!(records)
id_duplicates = records.group_by(&:id).select { |_id, group| group.length > 1 }
raise "duplicate legacy canonical IDs: #{id_duplicates.keys.join(', ')}" unless id_duplicates.empty?
path_lookup = records.to_h { |record| [record.path.to_s, record.id] }
name_lookup = build_name_lookup(records)
public_id_to_canonical = {}
manifest_by_public_id = manifest.fetch('entries').to_h { |entry| [entry.fetch('id'), entry] }
records.each { |record| public_id_to_canonical[record.public_entry['id']] = record.id if record.public_entry }
records.each { |record| transform_record!(record, records, path_lookup, name_lookup, public_id_to_canonical, manifest_by_public_id) }
validate_cross_record!(records)
validate_asset_paths!(records)
write_records!(records)
export_metadata!(records)
write_report!(records)
puts JSON.pretty_generate(records: records.length, migrated: REPORT[:migrated].length, created: REPORT[:created], public_projections: REPORT[:public_projections].length, unresolved_relationship_values: REPORT[:unresolved_relationship_values].length, preserved_unknown_fields: REPORT[:preserved_unknown_legacy_fields].length, skipped_missing_assets: REPORT[:skipped_missing_assets].length, slug_adjustments: REPORT[:slug_adjustments].length)
