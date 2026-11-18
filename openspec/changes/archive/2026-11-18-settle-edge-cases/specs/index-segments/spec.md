## ADDED Requirements

### Requirement: A rebuild does not rewrite a sealed segment
An implementation that rebuilds the index SHALL write the root and any segment that is missing, and SHALL NOT rewrite a segment that exists. Where the number of files in a sealed month's directory differs from the `count` recorded for its segment, the rebuild SHALL fail, naming each file that has no entry in the segment and each entry that has no file, and SHALL leave the segment as it was. The specification SHALL state that the index is reconstructible from the files in a workspace with no late merge, and that a late merge is repaired by re-minting, not by rebuilding.

#### Scenario: A rebuild after a late merge
- **WHEN** a merge has added two files to `episodes/2026-09/`, whose segment records `count: 412`, and the index is rebuilt
- **THEN** the rebuild fails, naming the two files, and `index/2026-09.yaml` is unchanged

#### Scenario: A rebuild with no late merge
- **WHEN** `index.yaml` is deleted from a workspace whose sealed months each match their segment's `count`, and the index is rebuilt
- **THEN** the root is written again, and no segment changes

#### Scenario: A missing segment
- **WHEN** a sealed month has files and no segment, and the index is rebuilt
- **THEN** the rebuild writes the segment, and the root lists its `path` and `count`

#### Scenario: A file removed from a sealed month
- **WHEN** a sealed month's directory holds one file fewer than its segment's `count`, and the index is rebuilt
- **THEN** the rebuild fails, naming the entry that has no file

### Requirement: A sealed month with no files has no segment
An implementation SHALL NOT write a segment, or an entry in `segments`, for a sealed month whose directory holds no files. A validator SHALL NOT report a segment as missing for such a month.

#### Scenario: A month in which nothing was recorded
- **WHEN** a workspace holds episodes minted in 2026-07 and 2026-11 and none between, and the index is built
- **THEN** `segments` lists `index/2026-07.yaml` and no segment for 2026-08 or 2026-09

#### Scenario: Two implementations index the same files
- **WHEN** two conformant implementations build the index of one set of files
- **THEN** their `segments` lists hold the same paths and counts
