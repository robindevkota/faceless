# Graph Report - .  (2026-04-13)

## Corpus Check
- 6 files · ~6,095 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 27 nodes · 33 edges · 6 communities detected
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]

## God Nodes (most connected - your core abstractions)
1. `main()` - 4 edges
2. `main()` - 4 edges
3. `main()` - 4 edges
4. `start_upload_session()` - 3 edges
5. `upload_video_chunk()` - 3 edges
6. `finish_upload()` - 3 edges
7. `main()` - 3 edges
8. `download_file()` - 2 edges
9. `fetch_pixabay_videos()` - 2 edges
10. `fetch_pixabay_music()` - 2 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Communities

### Community 0 - "Community 0"
Cohesion: 0.36
Nodes (7): finish_upload(), main(), Initialize a resumable upload session, return upload_session_id., Upload the video file in one chunk., Finalize the upload and publish the video., start_upload_session(), upload_video_chunk()

### Community 1 - "Community 1"
Cohesion: 0.7
Nodes (4): download_file(), fetch_pixabay_music(), fetch_pixabay_videos(), main()

### Community 2 - "Community 2"
Cohesion: 0.7
Nodes (4): build_metadata(), get_access_token(), main(), upload_video()

### Community 3 - "Community 3"
Cohesion: 0.83
Nodes (3): init_upload(), main(), upload_chunk()

### Community 4 - "Community 4"
Cohesion: 1.0
Nodes (2): generate_voice(), main()

### Community 5 - "Community 5"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **3 isolated node(s):** `Initialize a resumable upload session, return upload_session_id.`, `Upload the video file in one chunk.`, `Finalize the upload and publish the video.`
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 5`** (2 nodes): `main()`, `gemini_script.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What connects `Initialize a resumable upload session, return upload_session_id.`, `Upload the video file in one chunk.`, `Finalize the upload and publish the video.` to the rest of the system?**
  _3 weakly-connected nodes found - possible documentation gaps or missing edges._