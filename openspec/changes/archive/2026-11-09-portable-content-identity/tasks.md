## 1. `content.uid`

- [x] 1.1 Add `uid` to the reference `content` example in README.md, with an email `mid:` value and `media_type: message/rfc822`, and add `uid` to the calendar example.
- [x] 1.2 Add a paragraph to the `content` section defining `uid`:
  - the content's own identifier, written as a URI where the format defines one and verbatim otherwise;
  - the `mid:` transformation, with an example;
  - the iCalendar `UID`, written verbatim;
  - `media_type` is required with it;
  - `uid` is identity and `ref` is location;
  - writers record it whenever the source exposes one;
  - inline episodes do not carry it;
  - the recurring-event limit.
- [x] 1.3 In `source_status`, say that a reader may find content again by `uid`, that content found this way is not `gone`, and that `ref` is not rewritten. Adjust the definition of `gone` to match.
- [x] 1.4 State that a validator may report possible duplicates sharing `standpoint`, `media_type` and `uid`, and never rejects them.

## 2. Redaction and index

- [x] 2.1 Add `content.uid` to the closed redactable set.
- [x] 2.2 Add `content.uid` to the `index.yaml` sentence listing what never enters the index, if it is not already covered by "`content`".

## 3. Status and references

- [x] 3.1 Update the *Duplicate recordings* open question: `uid` makes aliases of one thing detectable, and what writers do about a duplicate is still open.
- [x] 3.2 Add RFC 2392 (`mid:`) and RFC 5322 (`Message-ID`) to References. RFC 5545 is already cited, so mention the `UID` there.
- [x] 3.3 Proofread, and run `openspec validate portable-content-identity`.
