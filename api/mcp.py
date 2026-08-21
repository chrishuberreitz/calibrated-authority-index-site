"""MCP Streamable HTTP endpoint for the Calibrated Authority Index.

POST /api/mcp — JSON-RPC 2.0 over HTTP per the MCP Streamable HTTP transport
(plain-JSON response mode; no SSE stream — stateless serverless). Methods:
initialize / tools/list / tools/call / ping. Notifications get HTTP 202.

Tool handlers are ported from the local stdio server
(~/.local/lib/ca_index_mcp/server.py) — same transport-agnostic logic. The
serverless function has no engine and no state directory, so the corpus travels
WITH the code, in the GENERATED CORPUS block below. That block is rewritten from
the released corpus by every `ca-index export --public`, exactly like
index.json / data.csv / llms.txt. It is not a snapshot anyone maintains by
hand; hand-editing it is a no-op the next export erases.

Every payload carries a `dataset` block naming the version and size of the
corpus that answered, plus the URL of the live dataset. The Index scores
institutions on D1 — traceability and inspectability — so its own agent surface
has to be checkable without an agent having to think to call a second tool.

Stdlib-only; Vercel Python runtime.

Connect an agent:
    claude mcp add --transport http ca-index \
        https://calibrated-authority.chrishuberreitz.com/api/mcp
"""
import json
from http.server import BaseHTTPRequestHandler

PROTOCOL_DEFAULT = "2025-03-26"
SUPPORTED_PROTOCOLS = ("2024-11-05", "2025-03-26", "2025-06-18")
SERVER_NAME = "calibrated-authority-index"
SERVER_VERSION = "1.0.0"
ENGINE_VERSION = "1.0.0"
_BASE_URL = "https://calibrated-authority.chrishuberreitz.com"
DATASET_NAME = "The Calibrated Authority Index"

DIMENSIONS = ["D1", "D2", "D3", "D4", "D5", "D6"]
DIM_LABELS = {
    "D1": "Traceability & inspectability",
    "D2": "Human authorship & accountability",
    "D3": "Disclosure & labeling",
    "D4": "Synthetic-identity / fabrication prohibition",
    "D5": "Human validation in loop",
    "D6": "Evidential-trust emphasis",
}

# --- BEGIN GENERATED CORPUS — ca-index export --public ---------------------
# Everything between these markers is re-derived from the released corpus on
# every export. Do NOT hand-edit: the next export overwrites it, and a number
# typed here is a number this endpoint would still be reporting long after the
# corpus had moved. Change the corpus, then export.
CORPUS_VERSION = "2026-08-21"
CORPUS_N = 69
CORPUS_GENERATED_AT = "2026-08-21T11:30:00Z"
_CORPUS_JSON = "[{\"c2_fit\":\"fits\",\"c3\":\"Both-split\",\"ca\":12,\"coded_date\":\"2026-08-09\",\"id\":\"uf-cpic\",\"last_changed\":\"2026-08-09\",\"name\":\"UF Center for Public Interest Communications\",\"posture\":\"Prohibitive\",\"provenance\":{\"url\":\"https://realgoodcenter.jou.ufl.edu/about/ai/\",\"verify_status\":\"primary-live-2026-08-09\"},\"quote\":\"All Center content must be replicable, evidence-based and traceable to sources that a human researcher can locate, review and re-create using documented methods.\",\"quote_label\":\"Our Approach to Generative Artificial Intelligence (updated 2026-03-09)\",\"revision\":3,\"scores\":{\"D1\":2,\"D2\":2,\"D3\":2,\"D4\":2,\"D5\":2,\"D6\":2},\"segment\":\"research-center\",\"twilight\":true,\"url\":\"https://realgoodcenter.jou.ufl.edu/about/ai/\"},{\"c2_fit\":\"fits\",\"c3\":\"Both-split\",\"ca\":12,\"coded_date\":\"2026-08-09\",\"id\":\"springer-nature\",\"last_changed\":\"2026-08-09\",\"name\":\"Springer Nature / Nature\",\"posture\":\"Balanced\",\"provenance\":{\"url\":\"https://www.nature.com/nature-portfolio/editorial-policies/ai\",\"verify_status\":\"primary-live-2026-08-09\"},\"quote\":\"Scholarly judgement, accountability, and responsibility always remain human.\",\"quote_label\":\"Nature Portfolio editorial policies \\u2014 Artificial Intelligence (AI), risk-assessment framework (live 2026-08-09)\",\"revision\":1,\"scores\":{\"D1\":2,\"D2\":2,\"D3\":2,\"D4\":2,\"D5\":2,\"D6\":2},\"segment\":\"publisher\",\"twilight\":true,\"url\":\"https://www.nature.com/nature-portfolio/editorial-policies/ai\"},{\"c2_fit\":\"fits\",\"c3\":\"Both-split\",\"ca\":12,\"coded_date\":\"2026-08-02\",\"id\":\"elsevier\",\"last_changed\":\"2026-08-02\",\"name\":\"Elsevier\",\"posture\":\"Balanced\",\"provenance\":{\"url\":\"https://www.elsevier.com/about/policies-and-standards/the-use-of-generative-ai-and-ai-assisted-technologies-in-writing-for-elsevier\",\"verify_status\":\"ok\"},\"quote\":\"Authorship implies responsibilities and tasks that can only be attributed to and performed by humans.\",\"quote_label\":\"Elsevier \\u2014 The use of generative AI and AI-assisted technologies in writing for Elsevier\",\"revision\":1,\"scores\":{\"D1\":2,\"D2\":2,\"D3\":2,\"D4\":2,\"D5\":2,\"D6\":2},\"segment\":\"publisher\",\"twilight\":false,\"url\":\"https://www.elsevier.com/about/policies-and-standards/the-use-of-generative-ai-and-ai-assisted-technologies-in-writing-for-elsevier\"},{\"c2_fit\":\"fits\",\"c3\":\"Both-split\",\"ca\":12,\"coded_date\":\"2026-07-26\",\"id\":\"wiley\",\"last_changed\":\"2026-07-26\",\"name\":\"Wiley\",\"posture\":\"Enabling\",\"provenance\":{\"url\":\"https://authorservices.wiley.com/ethics-guidelines/index.html\",\"verify_status\":\"primary-live-2026-07-26\"},\"quote\":\"Authors may only use AI Technology as an additional tool in their writing process, not a replacement for their own expertise and judgement.\",\"quote_label\":\"Wiley Best Practice Guidelines on Research Integrity and Publishing Ethics \\u2014 Artificial Intelligence, Human Oversight\",\"revision\":1,\"scores\":{\"D1\":2,\"D2\":2,\"D3\":2,\"D4\":2,\"D5\":2,\"D6\":2},\"segment\":\"publisher\",\"twilight\":true,\"url\":\"https://authorservices.wiley.com/ethics-guidelines/index.html\"},{\"c2_fit\":\"fits\",\"c3\":\"Both-split\",\"ca\":12,\"coded_date\":\"2026-06-22\",\"id\":\"taylor-francis\",\"last_changed\":null,\"name\":\"Taylor & Francis\",\"posture\":\"Enabling\",\"provenance\":{\"url\":\"https://taylorandfrancis.com/our-policies/ai-policy/\",\"verify_status\":\"primary-verified-2026-06-22\"},\"quote\":\"Generative AI tools must not be listed as an author because such tools are unable to assume responsibility for the submitted content or manage copyright and licensing agreements. These are uniquely human responsibilities that cannot be undertaken by Generative AI tools.\",\"quote_label\":\"AI policy (browser-verified 2026-06-22)\",\"revision\":0,\"scores\":{\"D1\":2,\"D2\":2,\"D3\":2,\"D4\":2,\"D5\":2,\"D6\":2},\"segment\":\"publisher\",\"twilight\":true,\"url\":\"https://taylorandfrancis.com/our-policies/ai-policy/\"},{\"c2_fit\":\"fits\",\"c3\":\"Both-split\",\"ca\":10,\"coded_date\":\"2026-07-26\",\"id\":\"science-aaas\",\"last_changed\":\"2026-07-26\",\"name\":\"Science / AAAS\",\"posture\":\"Balanced\",\"provenance\":{\"note\":\"Live page hard-403s automated fetch (no Chrome available this run); policy re-read in full from Wayback 2026-06-14 capture, which renders the complete editorial-policies text.\",\"url\":\"https://www.science.org/content/page/science-journals-editorial-policies\",\"verify_status\":\"secondary-wayback-2026-06-14 (live 403; Chrome unavailable this run)\"},\"quote\":\"AI-assisted technologies [such as large language models (LLMs), chatbots, and image creators] do not meet the Science journals' criteria for authorship and therefore may not be listed as authors or coauthors, nor may sources cited in Science journal content be authored or coauthored by AI tools.\",\"quote_label\":\"Science journals: editorial policies, Artificial intelligence (AI)\",\"revision\":2,\"scores\":{\"D1\":1,\"D2\":2,\"D3\":2,\"D4\":2,\"D5\":2,\"D6\":1},\"segment\":\"publisher\",\"twilight\":true,\"url\":\"https://www.science.org/content/page/science-journals-editorial-policies\"},{\"c2_fit\":\"fits\",\"c3\":\"Both-split\",\"ca\":12,\"coded_date\":\"2026-06-22\",\"id\":\"icmje\",\"last_changed\":null,\"name\":\"ICMJE\",\"posture\":\"Balanced\",\"provenance\":{\"url\":\"https://www.icmje.org/recommendations/browse/roles-and-responsibilities/defining-the-role-of-authors-and-contributors.html\",\"verify_status\":\"ok\"},\"quote\":\"Chatbots (such as ChatGPT) should not be listed as authors because they cannot be responsible for the accuracy, integrity, and originality of the work, and these responsibilities are required for authorship.\",\"quote_label\":\"Recommendations \\u2014 AI by authors\",\"revision\":0,\"scores\":{\"D1\":2,\"D2\":2,\"D3\":2,\"D4\":2,\"D5\":2,\"D6\":2},\"segment\":\"med-integrity\",\"twilight\":false,\"url\":\"https://www.icmje.org/recommendations/browse/roles-and-responsibilities/defining-the-role-of-authors-and-contributors.html\"},{\"c2_fit\":\"fits\",\"c3\":\"Relational\",\"ca\":7,\"coded_date\":\"2026-07-26\",\"id\":\"cope\",\"last_changed\":\"2026-07-26\",\"name\":\"COPE\",\"posture\":\"Balanced\",\"provenance\":{\"url\":\"https://publicationethics.org/guidance/cope-position/authorship-and-ai-tools\",\"verify_status\":\"secondary-wayback-2026-02-08 (live 403; Chrome unavailable this run)\"},\"quote\":\"AI tools cannot meet the requirements for authorship as they cannot take responsibility for the submitted work. As non-legal entities, they cannot assert the presence or absence of conflicts of interest nor manage copyright and license agreements.\",\"quote_label\":\"COPE position statement \\u2014 Authorship and AI tools\",\"revision\":1,\"scores\":{\"D1\":1,\"D2\":2,\"D3\":2,\"D4\":0,\"D5\":1,\"D6\":1},\"segment\":\"pub-ethics\",\"twilight\":false,\"url\":\"https://publicationethics.org/guidance/cope-position/authorship-and-ai-tools\"},{\"c2_fit\":\"fits\",\"c3\":\"Evidential\",\"ca\":12,\"coded_date\":\"2026-06-22\",\"id\":\"plos\",\"last_changed\":null,\"name\":\"PLOS\",\"posture\":\"Balanced\",\"provenance\":{\"url\":\"https://journals.plos.org/plosone/s/ethical-publishing-practice\",\"verify_status\":\"primary-verified-2026-06-22\"},\"quote\":\"The use of AI tools and technologies to fabricate or otherwise misrepresent primary research data is unacceptable.\",\"quote_label\":\"Ethical publishing practice (browser-verified)\",\"revision\":0,\"scores\":{\"D1\":2,\"D2\":2,\"D3\":2,\"D4\":2,\"D5\":2,\"D6\":2},\"segment\":\"publisher\",\"twilight\":false,\"url\":\"https://journals.plos.org/plosone/s/ethical-publishing-practice\"},{\"c2_fit\":\"fits\",\"c3\":\"Evidential\",\"ca\":12,\"coded_date\":\"2026-07-26\",\"id\":\"poynter\",\"last_changed\":\"2026-07-26\",\"name\":\"Poynter Institute\",\"posture\":\"Balanced\",\"provenance\":{\"note\":\"Guidelines page 403s automated fetch; page verified via Wayback 2026-07-09 capture - it is now a landing page for the 2025 AI Ethics Starter Kit. The kit's full policy template (published Google Doc, last updated 2025-06-01) and the public-facing PDF were fetched live and read in full; the coded quote is present verbatim in the template.\",\"url\":\"https://www.poynter.org/ai-ethics-journalism/ai-ethics-guidelines/\",\"verify_status\":\"secondary-wayback-2026-07-23 \\u2192 primary kit PDF (live 403; Chrome unavailable this run)\"},\"quote\":\"Our journalists remain responsible for everything we produce and publish, and we strive to verify anything created with generative AI that you see.\",\"quote_label\":\"AI Ethics Starter Kit \\u2014 public-facing generative AI policy template (2025 update)\",\"revision\":2,\"scores\":{\"D1\":2,\"D2\":2,\"D3\":2,\"D4\":2,\"D5\":2,\"D6\":2},\"segment\":\"journalism\",\"twilight\":true,\"url\":\"https://www.poynter.org/ai-ethics-journalism/ai-ethics-guidelines/\"},{\"c2_fit\":\"partially\",\"c3\":\"Both-split\",\"ca\":5,\"coded_date\":\"2026-06-28\",\"id\":\"reuters-institute\",\"last_changed\":null,\"name\":\"Reuters Institute (Oxford)\",\"posture\":\"Balanced\",\"provenance\":{\"url\":\"https://reutersinstitute.politics.ox.ac.uk/generative-ai-and-news-report-2025-how-people-think-about-ais-role-journalism-and-society\",\"verify_status\":\"ok\"},\"quote\":\"You cannot simply 'hack' your way to trust.\",\"quote_label\":\"Generative AI and news report 2025\",\"revision\":0,\"scores\":{\"D1\":1,\"D2\":1,\"D3\":1,\"D4\":0,\"D5\":1,\"D6\":1},\"segment\":\"journalism-research\",\"twilight\":true,\"url\":\"https://reutersinstitute.politics.ox.ac.uk/generative-ai-and-news-report-2025-how-people-think-about-ais-role-journalism-and-society\"},{\"c2_fit\":\"fits\",\"c3\":\"Both-split\",\"ca\":8,\"coded_date\":\"2026-06-22\",\"id\":\"columbia-tow\",\"last_changed\":null,\"name\":\"Columbia / Tow Center\",\"posture\":\"Balanced\",\"provenance\":{\"url\":\"https://journalism.columbia.edu/CJS2030/AI\",\"verify_status\":\"ok\"},\"quote\":\"We won't publish a story if our only source is AI \\u2014 it's not a substitute for the careful review of journalists.\",\"quote_label\":\"Tow Center / CJR\",\"revision\":0,\"scores\":{\"D1\":1,\"D2\":2,\"D3\":1,\"D4\":1,\"D5\":2,\"D6\":1},\"segment\":\"journalism-research\",\"twilight\":true,\"url\":\"https://journalism.columbia.edu/CJS2030/AI\"},{\"c2_fit\":\"fits\",\"c3\":\"Evidential\",\"ca\":10,\"coded_date\":\"2026-06-22\",\"id\":\"ap\",\"last_changed\":null,\"name\":\"Associated Press\",\"posture\":\"Balanced\",\"provenance\":{\"url\":\"https://ds.svcs.associatedpress.com/standards-around-generative-ai\",\"verify_status\":\"secondary-blocked\"},\"quote\":\"Any output from a generative AI tool should be treated as unvetted source material.\",\"quote_label\":\"Standards around generative AI (via Poynter/Globe reprint)\",\"revision\":0,\"scores\":{\"D1\":1,\"D2\":2,\"D3\":1,\"D4\":2,\"D5\":2,\"D6\":2},\"segment\":\"journalism\",\"twilight\":false,\"url\":\"https://ds.svcs.associatedpress.com/standards-around-generative-ai\"},{\"c2_fit\":\"fits\",\"c3\":\"Evidential\",\"ca\":8,\"coded_date\":\"2026-07-26\",\"id\":\"harvard\",\"last_changed\":\"2026-07-26\",\"name\":\"Harvard University\",\"posture\":\"Balanced\",\"provenance\":{\"url\":\"https://provost.harvard.edu/guidelines-using-chatgpt-and-other-generative-ai-tools-harvard\",\"verify_status\":\"secondary-wayback-2026-03-28 (live 403; Chrome unavailable this run)\"},\"quote\":\"You are responsible for any content that you produce or publish that includes AI-generated material.\",\"quote_label\":\"Guidelines for Using ChatGPT and other Generative AI tools at Harvard\",\"revision\":1,\"scores\":{\"D1\":1,\"D2\":2,\"D3\":1,\"D4\":1,\"D5\":2,\"D6\":1},\"segment\":\"university\",\"twilight\":true,\"url\":\"https://provost.harvard.edu/guidelines-using-chatgpt-and-other-generative-ai-tools-harvard\"},{\"c2_fit\":\"fits\",\"c3\":\"Both-split\",\"ca\":9,\"coded_date\":\"2026-06-22\",\"id\":\"stanford\",\"last_changed\":null,\"name\":\"Stanford University\",\"posture\":\"Balanced\",\"provenance\":{\"url\":\"https://communitystandards.stanford.edu/policies-guidance\",\"verify_status\":\"ok\"},\"quote\":\"Absent a clear statement from a course instructor, use of or consultation with generative AI shall be treated analogously to assistance from another person.\",\"quote_label\":\"Office of Community Standards\",\"revision\":0,\"scores\":{\"D1\":1,\"D2\":2,\"D3\":2,\"D4\":1,\"D5\":1,\"D6\":2},\"segment\":\"university\",\"twilight\":true,\"url\":\"https://communitystandards.stanford.edu/policies-guidance\"},{\"c2_fit\":\"fits\",\"c3\":\"Evidential\",\"ca\":8,\"coded_date\":\"2026-06-22\",\"id\":\"mit\",\"last_changed\":null,\"name\":\"MIT\",\"posture\":\"Balanced\",\"provenance\":{\"url\":\"https://ist.mit.edu/ai-guidance\",\"verify_status\":\"ok\"},\"quote\":\"You are responsible for the accuracy of any information you publish, including AI-generated content.\",\"quote_label\":\"IS&T AI guidance\",\"revision\":0,\"scores\":{\"D1\":1,\"D2\":2,\"D3\":2,\"D4\":1,\"D5\":1,\"D6\":1},\"segment\":\"university\",\"twilight\":true,\"url\":\"https://ist.mit.edu/ai-guidance\"},{\"c2_fit\":\"fits\",\"c3\":\"Evidential\",\"ca\":10,\"coded_date\":\"2026-06-22\",\"id\":\"umich\",\"last_changed\":null,\"name\":\"University of Michigan\",\"posture\":\"Enabling\",\"provenance\":{\"url\":\"https://genai.umich.edu/resources/faculty/course-policies\",\"verify_status\":\"ok\"},\"quote\":\"All data shared with U-M's AI services is private and will not be used to train AI models.\",\"quote_label\":\"ITS AI services\",\"revision\":0,\"scores\":{\"D1\":2,\"D2\":2,\"D3\":1,\"D4\":1,\"D5\":2,\"D6\":2},\"segment\":\"university\",\"twilight\":true,\"url\":\"https://genai.umich.edu/resources/faculty/course-policies\"},{\"c2_fit\":\"partially\",\"c3\":\"Evidential\",\"ca\":7,\"coded_date\":\"2026-07-12\",\"id\":\"russell-group\",\"last_changed\":\"2026-07-12\",\"name\":\"Russell Group (UK)\",\"posture\":\"Enabling\",\"provenance\":{\"url\":\"https://www.russellgroup.ac.uk/policy/policy-briefings/principles-use-generative-ai-tools-education\",\"verify_status\":\"ok\"},\"quote\":\"This means that accountability for the accuracy of information generated by these tools when transferred to another context lies with the user.\",\"quote_label\":\"Russell Group principles on generative AI in education, sec. 1.1(c) (full principles PDF)\",\"revision\":1,\"scores\":{\"D1\":1,\"D2\":1,\"D3\":1,\"D4\":1,\"D5\":1,\"D6\":2},\"segment\":\"university-consortium\",\"twilight\":false,\"url\":\"https://www.russellgroup.ac.uk/policy/policy-briefings/principles-use-generative-ai-tools-education\"},{\"c2_fit\":\"fits\",\"c3\":\"Both-split\",\"ca\":10,\"coded_date\":\"2026-06-22\",\"id\":\"mla-cccc\",\"last_changed\":null,\"name\":\"MLA-CCCC Task Force\",\"posture\":\"Balanced\",\"provenance\":{\"url\":\"https://aiandwriting.hcommons.org/working-paper-1/\",\"verify_status\":\"ok\"},\"quote\":\"We and others would caution against using LLMs to assess student writing or to write tailored feedback to students, given the danger of undermining trust and human connection in the classroom.\",\"quote_label\":\"Joint Task Force, Working Paper 3\",\"revision\":0,\"scores\":{\"D1\":2,\"D2\":2,\"D3\":2,\"D4\":1,\"D5\":2,\"D6\":1},\"segment\":\"education\",\"twilight\":false,\"url\":\"https://aiandwriting.hcommons.org/working-paper-1/\"},{\"c2_fit\":\"fits\",\"c3\":\"Both-split\",\"ca\":11,\"coded_date\":\"2026-07-26\",\"id\":\"acm\",\"last_changed\":\"2026-07-26\",\"name\":\"ACM\",\"posture\":\"Balanced\",\"provenance\":{\"note\":\"Policy updated 2026-05-14: AI writing-assistance disclosure no longer required (research-use still must be described in Methods). D3 2->1; CA 10->11.\",\"url\":\"https://www.acm.org/publications/policies/new-acm-policy-on-authorship\",\"verify_status\":\"secondary-wayback-2026-05-31 (live 403; Chrome unavailable this run)\"},\"quote\":\"When using Artificial Intelligence to assist with writing an ACM submission, ACM no longer requires the disclosure of information regarding the use of AI.\",\"quote_label\":\"ACM Policy on Authorship, Use of Artificial Intelligence\",\"revision\":1,\"scores\":{\"D1\":2,\"D2\":2,\"D3\":1,\"D4\":2,\"D5\":2,\"D6\":2},\"segment\":\"computing-society\",\"twilight\":false,\"url\":\"https://www.acm.org/publications/policies/new-acm-policy-on-authorship\"},{\"c2_fit\":\"fits\",\"c3\":\"Both-split\",\"ca\":11,\"coded_date\":\"2026-06-22\",\"id\":\"apa\",\"last_changed\":null,\"name\":\"APA\",\"posture\":\"Balanced\",\"provenance\":{\"url\":\"https://www.apa.org/pubs/journals/resources/publishing-tips/policy-generative-ai\",\"verify_status\":\"ok\"},\"quote\":\"AI is not a conscious human who can consent to the duties and responsibilities of authorship, which include responsibility for post publication changes such as corrections or retractions.\",\"quote_label\":\"Journals generative-AI policy\",\"revision\":0,\"scores\":{\"D1\":2,\"D2\":2,\"D3\":2,\"D4\":2,\"D5\":2,\"D6\":1},\"segment\":\"society-publisher\",\"twilight\":false,\"url\":\"https://www.apa.org/pubs/journals/resources/publishing-tips/policy-generative-ai\"},{\"c2_fit\":\"fits\",\"c3\":\"Both-split\",\"ca\":9,\"coded_date\":\"2026-06-22\",\"id\":\"yale\",\"last_changed\":null,\"name\":\"Yale University\",\"posture\":\"Balanced\",\"provenance\":{\"url\":\"https://provost.yale.edu/news/guidelines-use-generative-ai-tools\",\"verify_status\":\"ok\"},\"quote\":\"Always review and verify outputs generated by AI tools, especially before publication. We are each responsible for the content of our work product.\",\"quote_label\":\"Provost guidelines\",\"revision\":0,\"scores\":{\"D1\":1,\"D2\":2,\"D3\":2,\"D4\":1,\"D5\":2,\"D6\":1},\"segment\":\"university\",\"twilight\":false,\"url\":\"https://provost.yale.edu/news/guidelines-use-generative-ai-tools\"},{\"c2_fit\":\"fits\",\"c3\":\"Both-split\",\"ca\":11,\"coded_date\":\"2026-07-26\",\"id\":\"princeton\",\"last_changed\":\"2026-07-26\",\"name\":\"Princeton University\",\"posture\":\"Balanced\",\"provenance\":{\"url\":\"https://rrr.princeton.edu/students-and-university/24-academic-regulations\",\"verify_status\":\"secondary-wayback-2026-07-20 (live 403; Chrome unavailable this run)\"},\"quote\":\"Generative AI is not a source as defined in this provision because its output is not created by a person.\",\"quote_label\":\"Rights, Rules, Responsibilities 2.4.7, Generative AI\",\"revision\":1,\"scores\":{\"D1\":2,\"D2\":2,\"D3\":2,\"D4\":2,\"D5\":1,\"D6\":2},\"segment\":\"university\",\"twilight\":false,\"url\":\"https://rrr.princeton.edu/students-and-university/24-academic-regulations\"},{\"c2_fit\":\"partially\",\"c3\":\"Evidential\",\"ca\":6,\"coded_date\":\"2026-06-22\",\"id\":\"uc-berkeley\",\"last_changed\":null,\"name\":\"University of California, Berkeley\",\"posture\":\"Balanced\",\"provenance\":{\"url\":\"https://oercs.berkeley.edu/appropriate-use-generative-ai-tools\",\"verify_status\":\"ok\"},\"quote\":\"No personal, confidential, proprietary, or otherwise sensitive information may be entered into or generated as output from models.\",\"quote_label\":\"Appropriate use of generative AI\",\"revision\":0,\"scores\":{\"D1\":1,\"D2\":1,\"D3\":1,\"D4\":1,\"D5\":1,\"D6\":1},\"segment\":\"university\",\"twilight\":false,\"url\":\"https://oercs.berkeley.edu/appropriate-use-generative-ai-tools\"},{\"c2_fit\":\"fits\",\"c3\":\"Both-split\",\"ca\":8,\"coded_date\":\"2026-07-05\",\"id\":\"cornell\",\"last_changed\":null,\"name\":\"Cornell University\",\"posture\":\"Enabling\",\"provenance\":{\"url\":\"https://it.cornell.edu/ai/ai-guidelines\",\"verify_status\":\"ok\"},\"quote\":\"You are accountable for your work, regardless of the tools you use to produce it.\",\"quote_label\":\"AI guidelines\",\"revision\":0,\"scores\":{\"D1\":1,\"D2\":2,\"D3\":1,\"D4\":1,\"D5\":2,\"D6\":1},\"segment\":\"university\",\"twilight\":false,\"url\":\"https://it.cornell.edu/ai/ai-guidelines\"},{\"c2_fit\":\"fits\",\"c3\":\"Both-split\",\"ca\":11,\"coded_date\":\"2026-06-22\",\"id\":\"carnegie-mellon\",\"last_changed\":null,\"name\":\"Carnegie Mellon University\",\"posture\":\"Prohibitive\",\"provenance\":{\"url\":\"https://www.cmu.edu/teaching/technology/aitools/academicintegrity/index.html\",\"verify_status\":\"ok\"},\"quote\":\"You are ultimately responsible for the content that you submit.\",\"quote_label\":\"Eberly Center course-policy examples\",\"revision\":0,\"scores\":{\"D1\":2,\"D2\":2,\"D3\":2,\"D4\":1,\"D5\":2,\"D6\":2},\"segment\":\"university\",\"twilight\":false,\"url\":\"https://www.cmu.edu/teaching/technology/aitools/academicintegrity/index.html\"},{\"c2_fit\":\"fits\",\"c3\":\"Evidential\",\"ca\":12,\"coded_date\":\"2026-06-22\",\"id\":\"georgia-tech\",\"last_changed\":null,\"name\":\"Georgia Institute of Technology\",\"posture\":\"Enabling\",\"provenance\":{\"url\":\"https://provost.gatech.edu/sites/default/files/2025-10/AI%20Policy_draft_10.14.2025%202.pdf\",\"verify_status\":\"ok\"},\"quote\":\"Core scholarly and research contributions are expected to remain under the full direction and responsibility of the GT community member.\",\"quote_label\":\"AI Policy (draft, 2025-10-14)\",\"revision\":0,\"scores\":{\"D1\":2,\"D2\":2,\"D3\":2,\"D4\":2,\"D5\":2,\"D6\":2},\"segment\":\"university\",\"twilight\":true,\"url\":\"https://provost.gatech.edu/sites/default/files/2025-10/AI%20Policy_draft_10.14.2025%202.pdf\"},{\"c2_fit\":\"fits\",\"c3\":\"Evidential\",\"ca\":11,\"coded_date\":\"2026-06-22\",\"id\":\"u-toronto\",\"last_changed\":null,\"name\":\"University of Toronto\",\"posture\":\"Balanced\",\"provenance\":{\"url\":\"https://www.viceprovostundergrad.utoronto.ca/wp-content/uploads/2024/08/Syllabus-language-for-Gen-AI-2024-08-21.pdf\",\"verify_status\":\"ok\"},\"quote\":\"Generative AI tools do not meet the criteria for authorship of scholarly works, because these tools cannot take responsibility or be held accountable for submitted work.\",\"quote_label\":\"SGS guidance\",\"revision\":0,\"scores\":{\"D1\":2,\"D2\":2,\"D3\":2,\"D4\":1,\"D5\":2,\"D6\":2},\"segment\":\"university\",\"twilight\":true,\"url\":\"https://www.viceprovostundergrad.utoronto.ca/wp-content/uploads/2024/08/Syllabus-language-for-Gen-AI-2024-08-21.pdf\"},{\"c2_fit\":\"fits\",\"c3\":\"Both-split\",\"ca\":9,\"coded_date\":\"2026-06-22\",\"id\":\"cambridge\",\"last_changed\":null,\"name\":\"University of Cambridge\",\"posture\":\"Balanced\",\"provenance\":{\"url\":\"https://www.educationalpolicy.admin.cam.ac.uk/plagiarism-and-academic-misconduct/artificial-intelligence-ai\",\"verify_status\":\"ok\"},\"quote\":\"A student using any unacknowledged content generated by artificial intelligence within a summative assessment as though it is their own work constitutes academic misconduct.\",\"quote_label\":\"AI and academic misconduct\",\"revision\":0,\"scores\":{\"D1\":1,\"D2\":2,\"D3\":2,\"D4\":1,\"D5\":2,\"D6\":1},\"segment\":\"university\",\"twilight\":true,\"url\":\"https://www.educationalpolicy.admin.cam.ac.uk/plagiarism-and-academic-misconduct/artificial-intelligence-ai\"},{\"c2_fit\":\"fits\",\"c3\":\"Both-split\",\"ca\":9,\"coded_date\":\"2026-06-22\",\"id\":\"ucl\",\"last_changed\":null,\"name\":\"University College London\",\"posture\":\"Enabling\",\"provenance\":{\"url\":\"https://www.ucl.ac.uk/teaching-learning/generative-ai-hub/three-categories-genai-use-assessment\",\"verify_status\":\"ok\"},\"quote\":\"The student should still be the author of their own work \\u2014 GenAI should be limited to supporting and assisting the student.\",\"quote_label\":\"Generative AI hub\",\"revision\":0,\"scores\":{\"D1\":1,\"D2\":2,\"D3\":2,\"D4\":1,\"D5\":2,\"D6\":1},\"segment\":\"university\",\"twilight\":true,\"url\":\"https://www.ucl.ac.uk/teaching-learning/generative-ai-hub/three-categories-genai-use-assessment\"},{\"c2_fit\":\"fits\",\"c3\":\"Both-split\",\"ca\":8,\"coded_date\":\"2026-06-22\",\"id\":\"asu\",\"last_changed\":null,\"name\":\"Arizona State University\",\"posture\":\"Balanced\",\"provenance\":{\"url\":\"https://tlc.sols.asu.edu/teaching/toolkits/syllabus-and-policies-generative-ai\",\"verify_status\":\"ok\"},\"quote\":\"Any submitted course assignment that does not explicitly articulate how generative AI was used will be assumed to have been created entirely without its use.\",\"quote_label\":\"Syllabus & policies on generative AI\",\"revision\":0,\"scores\":{\"D1\":1,\"D2\":2,\"D3\":2,\"D4\":0,\"D5\":2,\"D6\":1},\"segment\":\"university\",\"twilight\":true,\"url\":\"https://tlc.sols.asu.edu/teaching/toolkits/syllabus-and-policies-generative-ai\"},{\"c2_fit\":\"fits\",\"c3\":\"Both-split\",\"ca\":9,\"coded_date\":\"2026-06-22\",\"id\":\"cambridge-up\",\"last_changed\":null,\"name\":\"Cambridge University Press\",\"posture\":\"Balanced\",\"provenance\":{\"url\":\"https://www.cambridge.org/core/services/publishing-ethics/authorship-and-contributorship-journals\",\"verify_status\":\"ok\"},\"quote\":\"AI does not meet the Cambridge requirements for authorship, given the need for accountability.\",\"quote_label\":\"Authorship and contributorship policy\",\"revision\":0,\"scores\":{\"D1\":1,\"D2\":2,\"D3\":2,\"D4\":1,\"D5\":2,\"D6\":1},\"segment\":\"publisher\",\"twilight\":false,\"url\":\"https://www.cambridge.org/core/services/publishing-ethics/authorship-and-contributorship-journals\"},{\"c2_fit\":\"fits\",\"c3\":\"Evidential\",\"ca\":12,\"coded_date\":\"2026-06-22\",\"id\":\"oxford-up\",\"last_changed\":null,\"name\":\"Oxford University Press\",\"posture\":\"Balanced\",\"provenance\":{\"url\":\"https://academic.oup.com/pages/for-authors/books/author-use-of-artificial-intelligence\",\"verify_status\":\"ok\"},\"quote\":\"Gen AI does not qualify as an author and should not be used to undertake primary authorial responsibilities, such as generating arguments and scientific insights, writing analysis, or drawing conclusions.\",\"quote_label\":\"Author use of AI\",\"revision\":0,\"scores\":{\"D1\":2,\"D2\":2,\"D3\":2,\"D4\":2,\"D5\":2,\"D6\":2},\"segment\":\"publisher\",\"twilight\":true,\"url\":\"https://academic.oup.com/pages/for-authors/books/author-use-of-artificial-intelligence\"},{\"c2_fit\":\"fits\",\"c3\":\"Evidential\",\"ca\":12,\"coded_date\":\"2026-08-09\",\"id\":\"sage\",\"last_changed\":\"2026-08-09\",\"name\":\"SAGE Publishing\",\"posture\":\"Balanced\",\"provenance\":{\"url\":\"https://www.sagepub.com/journals/publication-ethics-policies/artificial-intelligence-policy\",\"verify_status\":\"primary-live-2026-08-09\"},\"quote\":\"We distinguish various uses for AI and related technologies as: assistive (and no longer requiring disclosure), generative (requiring disclosure), and prohibitive.\",\"quote_label\":\"Sage Journals \\u2014 Artificial intelligence policy (live 2026-08-09)\",\"revision\":1,\"scores\":{\"D1\":2,\"D2\":2,\"D3\":2,\"D4\":2,\"D5\":2,\"D6\":2},\"segment\":\"publisher\",\"twilight\":true,\"url\":\"https://www.sagepub.com/journals/publication-ethics-policies/artificial-intelligence-policy\"},{\"c2_fit\":\"fits\",\"c3\":\"Both-split\",\"ca\":11,\"coded_date\":\"2026-06-22\",\"id\":\"ieee\",\"last_changed\":null,\"name\":\"IEEE\",\"posture\":\"Balanced\",\"provenance\":{\"url\":\"https://open.ieee.org/author-guidelines-for-artificial-intelligence-ai-generated-text/\",\"verify_status\":\"ok\"},\"quote\":\"The use of content generated by artificial intelligence in an article shall be disclosed in the acknowledgments section.\",\"quote_label\":\"Author guidelines for AI-generated text\",\"revision\":0,\"scores\":{\"D1\":2,\"D2\":2,\"D3\":2,\"D4\":2,\"D5\":1,\"D6\":2},\"segment\":\"computing-society\",\"twilight\":false,\"url\":\"https://open.ieee.org/author-guidelines-for-artificial-intelligence-ai-generated-text/\"},{\"c2_fit\":\"fits\",\"c3\":\"Evidential\",\"ca\":12,\"coded_date\":\"2026-06-22\",\"id\":\"pnas\",\"last_changed\":null,\"name\":\"PNAS\",\"posture\":\"Balanced\",\"provenance\":{\"url\":\"https://www.pnas.org/author-center/editorial-and-journal-policies\",\"verify_status\":\"ok\"},\"quote\":\"The software cannot be listed as an author because it does not meet the criteria for authorship and cannot share responsibility for the paper or be held accountable for the integrity of the data reported.\",\"quote_label\":\"Editorial and journal policies\",\"revision\":0,\"scores\":{\"D1\":2,\"D2\":2,\"D3\":2,\"D4\":2,\"D5\":2,\"D6\":2},\"segment\":\"publisher\",\"twilight\":true,\"url\":\"https://www.pnas.org/author-center/editorial-and-journal-policies\"},{\"c2_fit\":\"fits\",\"c3\":\"Both-split\",\"ca\":10,\"coded_date\":\"2026-06-28\",\"id\":\"jama\",\"last_changed\":null,\"name\":\"JAMA Network\",\"posture\":\"Balanced\",\"provenance\":{\"url\":\"https://jamanetwork.com/journals/jama/fullarticle/2807956\",\"verify_status\":\"ok\"},\"quote\":\"Attribution of authorship carries with it accountability for the work, and AI tools cannot take such responsibility.\",\"quote_label\":\"Instructions for authors\",\"revision\":0,\"scores\":{\"D1\":2,\"D2\":2,\"D3\":2,\"D4\":1,\"D5\":1,\"D6\":2},\"segment\":\"med-journal\",\"twilight\":true,\"url\":\"https://jamanetwork.com/journals/jama/fullarticle/2807956\"},{\"c2_fit\":\"fits\",\"c3\":\"Both-split\",\"ca\":9,\"coded_date\":\"2026-06-22\",\"id\":\"nejm\",\"last_changed\":null,\"name\":\"New England Journal of Medicine\",\"posture\":\"Balanced\",\"provenance\":{\"url\":\"https://ai.nejm.org/about/editorial-policies\",\"verify_status\":\"ok\"},\"quote\":\"Because the authors of a manuscript are responsible for the accuracy, integrity, and originality of the work, chatbots or other AI-assisted technologies cannot be listed as authors.\",\"quote_label\":\"NEJM AI editorial policies\",\"revision\":0,\"scores\":{\"D1\":1,\"D2\":2,\"D3\":2,\"D4\":1,\"D5\":2,\"D6\":1},\"segment\":\"med-journal\",\"twilight\":false,\"url\":\"https://ai.nejm.org/about/editorial-policies\"},{\"c2_fit\":\"fits\",\"c3\":\"Both-split\",\"ca\":12,\"coded_date\":\"2026-06-22\",\"id\":\"wame\",\"last_changed\":null,\"name\":\"World Association of Medical Editors\",\"posture\":\"Balanced\",\"provenance\":{\"url\":\"https://wame.org/page3.php?id=106\",\"verify_status\":\"ok\"},\"quote\":\"In the interests of enabling scientific scrutiny, including replication and identifying falsification, the full prompt used to generate the research results, the time and date of query, and the AI tool used and its version, should be provided.\",\"quote_label\":\"Recommendations on chatbots & generative AI\",\"revision\":0,\"scores\":{\"D1\":2,\"D2\":2,\"D3\":2,\"D4\":2,\"D5\":2,\"D6\":2},\"segment\":\"med-integrity\",\"twilight\":true,\"url\":\"https://wame.org/page3.php?id=106\"},{\"c2_fit\":\"fits\",\"c3\":\"Both-split\",\"ca\":10,\"coded_date\":\"2026-06-22\",\"id\":\"cse\",\"last_changed\":null,\"name\":\"Council of Science Editors\",\"posture\":\"Balanced\",\"provenance\":{\"url\":\"https://www.csescienceeditor.org/article/cse-guidance-on-machine-learning-and-artificial-intelligence-tools/\",\"verify_status\":\"ok\"},\"quote\":\"A nonhuman cannot be responsible or accountable for the accuracy, integrity, and originality of the work.\",\"quote_label\":\"Guidance on machine learning and AI tools\",\"revision\":0,\"scores\":{\"D1\":2,\"D2\":2,\"D3\":2,\"D4\":1,\"D5\":1,\"D6\":2},\"segment\":\"science-editors\",\"twilight\":true,\"url\":\"https://www.csescienceeditor.org/article/cse-guidance-on-machine-learning-and-artificial-intelligence-tools/\"},{\"c2_fit\":\"fits\",\"c3\":\"Both-split\",\"ca\":10,\"coded_date\":\"2026-06-22\",\"id\":\"royal-society\",\"last_changed\":null,\"name\":\"The Royal Society\",\"posture\":\"Balanced\",\"provenance\":{\"url\":\"https://royalsociety.org/journals/ethics-policies/openness/\",\"verify_status\":\"ok\"},\"quote\":\"Such systems must not replace key researcher tasks such as producing scientific insights, analysing and interpreting data.\",\"quote_label\":\"Authorship, competing interests and AI\",\"revision\":0,\"scores\":{\"D1\":1,\"D2\":2,\"D3\":2,\"D4\":2,\"D5\":2,\"D6\":1},\"segment\":\"society-publisher\",\"twilight\":true,\"url\":\"https://royalsociety.org/journals/ethics-policies/openness/\"},{\"c2_fit\":\"fits\",\"c3\":\"Both-split\",\"ca\":12,\"coded_date\":\"2026-08-16\",\"id\":\"bbc\",\"last_changed\":\"2026-07-26\",\"name\":\"BBC\",\"posture\":\"Balanced\",\"provenance\":{\"note\":\"Re-verified live 2026-08-16 after the weekly scan flagged a change. Snapshot word-diff shows the flag was page furniture only, with zero change to policy text: a page build timestamp and build hash (\\\"Thu Jul 23 14:55:25\\\"/\\\"22ac427\\\" -> \\\"Wed Aug 12 12:17:42\\\"/\\\"106308a\\\") plus a new \\\"Careers\\\" nav link. The coded verbatim quote is still present word-for-word in the live document; scores unmoved.\",\"url\":\"https://www.bbc.co.uk/editorialguidelines/guidance/use-of-artificial-intelligence\",\"verify_status\":\"primary-live-2026-08-16\"},\"quote\":\"Any use of AI by the BBC in the creation, presentation or distribution of content must include active human editorial oversight and approval, appropriate to the nature of its use and consistent with the Editorial Guidelines.\",\"quote_label\":\"Guidance: The use of Artificial Intelligence\",\"revision\":2,\"scores\":{\"D1\":2,\"D2\":2,\"D3\":2,\"D4\":2,\"D5\":2,\"D6\":2},\"segment\":\"journalism\",\"twilight\":true,\"url\":\"https://www.bbc.co.uk/editorialguidelines/guidance/use-of-artificial-intelligence\"},{\"c2_fit\":\"fits\",\"c3\":\"Evidential\",\"ca\":11,\"coded_date\":\"2026-07-26\",\"id\":\"reuters-news\",\"last_changed\":\"2026-07-26\",\"name\":\"Reuters (news agency)\",\"posture\":\"Balanced\",\"provenance\":{\"url\":\"https://handbook.reuters.com/index.php?title=Standards_and_Values\",\"verify_status\":\"primary-live-2026-07-26\"},\"quote\":\"All facts, sources and claims generated by AI must be independently verified and fact-checked by Reuters journalists.\",\"quote_label\":\"Reuters Handbook of Journalism \\u2014 Standards and Values, Artificial Intelligence and Generative AI\",\"revision\":1,\"scores\":{\"D1\":2,\"D2\":2,\"D3\":1,\"D4\":2,\"D5\":2,\"D6\":2},\"segment\":\"journalism\",\"twilight\":false,\"url\":\"https://handbook.reuters.com/index.php?title=Standards_and_Values\"},{\"c2_fit\":\"fits\",\"c3\":\"Both-split\",\"ca\":11,\"coded_date\":\"2026-06-22\",\"id\":\"guardian\",\"last_changed\":null,\"name\":\"The Guardian\",\"posture\":\"Balanced\",\"provenance\":{\"url\":\"https://uploads.guim.co.uk/2026/03/03/Editorial_Code_of_Practice_Guidelines_March2026.pdf\",\"verify_status\":\"ok\"},\"quote\":\"Guardian audiences are entitled to expect that work that appears under your byline has been authored by you.\",\"quote_label\":\"Editorial Code \\u00a7H (2026-03)\",\"revision\":0,\"scores\":{\"D1\":2,\"D2\":2,\"D3\":2,\"D4\":1,\"D5\":2,\"D6\":2},\"segment\":\"journalism\",\"twilight\":true,\"url\":\"https://uploads.guim.co.uk/2026/03/03/Editorial_Code_of_Practice_Guidelines_March2026.pdf\"},{\"c2_fit\":\"fits\",\"c3\":\"Both-split\",\"ca\":12,\"coded_date\":\"2026-06-22\",\"id\":\"nyt\",\"last_changed\":null,\"name\":\"The New York Times\",\"posture\":\"Prohibitive\",\"provenance\":{\"url\":\"https://www.nytco.com/press/principles-for-using-generative-a.i.-in-the-timess-newsroom/\",\"verify_status\":\"secondary-blocked\"},\"quote\":\"We don't use A.I. to write articles, and journalists are ultimately responsible for everything that we publish.\",\"quote_label\":\"Newsroom principles (secondary-sourced)\",\"revision\":0,\"scores\":{\"D1\":2,\"D2\":2,\"D3\":2,\"D4\":2,\"D5\":2,\"D6\":2},\"segment\":\"journalism\",\"twilight\":true,\"url\":\"https://www.nytco.com/press/principles-for-using-generative-a.i.-in-the-timess-newsroom/\"},{\"c2_fit\":\"fits\",\"c3\":\"Evidential\",\"ca\":9,\"coded_date\":\"2026-08-09\",\"id\":\"spj\",\"last_changed\":\"2026-08-09\",\"name\":\"Society of Professional Journalists\",\"posture\":\"Balanced\",\"provenance\":{\"url\":\"https://www.spj.org/spj-code-of-ethics/\",\"verify_status\":\"primary-live-2026-08-09\"},\"quote\":\"Take responsibility for the accuracy of their work. Verify information before releasing it. Use original sources whenever possible.\",\"quote_label\":\"SPJ Code of Ethics, Seek Truth and Report It (2014 revision)\",\"revision\":3,\"scores\":{\"D1\":2,\"D2\":1,\"D3\":2,\"D4\":1,\"D5\":1,\"D6\":2},\"segment\":\"journalism\",\"twilight\":false,\"url\":\"https://www.spj.org/spj-code-of-ethics/\"},{\"c2_fit\":\"partially\",\"c3\":\"Both-split\",\"ca\":5,\"coded_date\":\"2026-06-22\",\"id\":\"arl\",\"last_changed\":null,\"name\":\"Association of Research Libraries\",\"posture\":\"Enabling\",\"provenance\":{\"url\":\"https://www.arl.org/resources/research-libraries-guiding-principles-for-artificial-intelligence/\",\"verify_status\":\"ok\"},\"quote\":\"Libraries believe 'no human, no AI.'\",\"quote_label\":\"Guiding Principles for AI\",\"revision\":0,\"scores\":{\"D1\":1,\"D2\":1,\"D3\":0,\"D4\":1,\"D5\":1,\"D6\":1},\"segment\":\"library\",\"twilight\":true,\"url\":\"https://www.arl.org/resources/research-libraries-guiding-principles-for-artificial-intelligence/\"},{\"c2_fit\":\"contradicts\",\"c3\":\"Relational\",\"ca\":3,\"coded_date\":\"2026-07-26\",\"id\":\"educause\",\"last_changed\":\"2026-07-26\",\"name\":\"EDUCAUSE\",\"posture\":\"Balanced\",\"provenance\":{\"note\":\"Live page now returns 403 to automated fetch (WebFetch and browser-UA curl); article re-read in full from Wayback capture 2026-05-05. Coded quote present verbatim; article body unchanged from the 2023-12-12 publication.\",\"url\":\"https://er.educause.edu/articles/2023/12/cross-campus-approaches-to-building-a-generative-ai-policy\",\"verify_status\":\"secondary-wayback-2026-05-05 (live 403; Chrome unavailable this run)\"},\"quote\":\"Beyond the problem of false accusations, this environment also creates an untenable situation for students who must somehow defend themselves against a machine that cannot show its work but is just a projection.\",\"quote_label\":\"Cross-Campus Approaches to Building a Generative AI Policy, EDUCAUSE Review\",\"revision\":2,\"scores\":{\"D1\":0,\"D2\":1,\"D3\":1,\"D4\":0,\"D5\":0,\"D6\":1},\"segment\":\"edtech\",\"twilight\":true,\"url\":\"https://er.educause.edu/articles/2023/12/cross-campus-approaches-to-building-a-generative-ai-policy\"},{\"c2_fit\":\"partially\",\"c3\":\"Relational\",\"ca\":9,\"coded_date\":\"2026-08-16\",\"id\":\"unesco\",\"last_changed\":\"2026-08-02\",\"name\":\"UNESCO \\u2014 GenAI in education & research\",\"posture\":\"Prohibitive\",\"provenance\":{\"note\":\"Re-verified live 2026-08-16 after the weekly scan flagged a change. Snapshot word-diff shows the flag was page furniture only, with zero change to policy text: the sidebar related-publications carousel rotated (e.g. \\\"Jordan\\u2019s Education Strategic Plan 2026\\u20132030\\\" -> \\\"Higher education global trends report\\\"). The coded verbatim quote is still present word-for-word in the live document; scores unmoved.\",\"url\":\"https://www.unesco.org/en/articles/guidance-generative-ai-education-and-research\",\"verify_status\":\"primary-live-2026-08-16\"},\"quote\":\"Publicly available generative AI (GenAI) tools are rapidly emerging, and the release of iterative versions is outpacing the adaptation of national regulatory frameworks.\",\"quote_label\":\"Guidance for generative AI in education and research (UNESCO)\",\"revision\":2,\"scores\":{\"D1\":1,\"D2\":2,\"D3\":1,\"D4\":2,\"D5\":2,\"D6\":1},\"segment\":\"intergov\",\"twilight\":true,\"url\":\"https://www.unesco.org/en/articles/guidance-generative-ai-education-and-research\"},{\"c2_fit\":\"fits\",\"c3\":\"Evidential\",\"ca\":10,\"coded_date\":\"2026-06-22\",\"id\":\"oecd\",\"last_changed\":null,\"name\":\"OECD AI Principles\",\"posture\":\"Enabling\",\"provenance\":{\"url\":\"https://oecd.ai/en/ai-principles\",\"verify_status\":\"ok\"},\"quote\":\"AI actors should ensure traceability, including in relation to datasets, processes and decisions made during the AI system lifecycle, to enable analysis of the AI system's outputs and responses to inquiry.\",\"quote_label\":\"AI Principles (OECD/LEGAL/0449)\",\"revision\":0,\"scores\":{\"D1\":2,\"D2\":2,\"D3\":2,\"D4\":1,\"D5\":1,\"D6\":2},\"segment\":\"intergov\",\"twilight\":false,\"url\":\"https://oecd.ai/en/ai-principles\"},{\"c2_fit\":\"partially\",\"c3\":\"Both-split\",\"ca\":8,\"coded_date\":\"2026-06-22\",\"id\":\"us-doe-oet\",\"last_changed\":null,\"name\":\"US Dept of Education (OET)\",\"posture\":\"Balanced\",\"provenance\":{\"url\":\"https://www.ed.gov/sites/ed/files/documents/ai-report/ai-report.pdf\",\"verify_status\":\"ok\"},\"quote\":\"A top priority with AI is to keep humans in the loop and in control.\",\"quote_label\":\"AI and the Future of Teaching and Learning\",\"revision\":0,\"scores\":{\"D1\":1,\"D2\":2,\"D3\":1,\"D4\":1,\"D5\":2,\"D6\":1},\"segment\":\"gov-education\",\"twilight\":true,\"url\":\"https://www.ed.gov/sites/ed/files/documents/ai-report/ai-report.pdf\"},{\"c2_fit\":\"fits\",\"c3\":\"Evidential\",\"ca\":8,\"coded_date\":\"2026-08-16\",\"id\":\"uspto\",\"last_changed\":\"2026-08-02\",\"name\":\"USPTO \\u2014 Inventorship Guidance for AI-Assisted Inventions\",\"posture\":\"Balanced\",\"provenance\":{\"note\":\"Re-verified live 2026-08-16 after the weekly scan flagged a change. Snapshot word-diff shows the flag was page furniture only, with zero change to policy text: the Federal Register page-view counter (29,204 -> 29,303) and the retrieval date stamp. Federal Register documents are immutable once published. The coded verbatim quote is still present word-for-word in the live document; scores unmoved.\",\"url\":\"https://www.federalregister.gov/documents/2024/02/13/2024-02623/inventorship-guidance-for-ai-assisted-inventions\",\"verify_status\":\"primary-live-2026-08-16\"},\"quote\":\"such inventions are not categorically unpatentable due to improper inventorship if one or more natural persons significantly contributed to the invention\",\"quote_label\":\"Inventorship Guidance for AI-Assisted Inventions, 89 FR 10043 (Feb. 13, 2024)\",\"revision\":2,\"scores\":{\"D1\":1,\"D2\":2,\"D3\":1,\"D4\":2,\"D5\":1,\"D6\":1},\"segment\":\"regulator\",\"twilight\":false,\"url\":\"https://www.federalregister.gov/documents/2024/02/13/2024-02623/inventorship-guidance-for-ai-assisted-inventions\"},{\"c2_fit\":\"partially\",\"c3\":\"Both-split\",\"ca\":8,\"coded_date\":\"2026-06-28\",\"id\":\"vatican-ddf\",\"last_changed\":null,\"name\":\"Vatican (DDF/DCE) \\u2014 Antiqua et Nova (2025)\",\"posture\":\"Balanced\",\"provenance\":{\"url\":\"https://www.vatican.va/roman_curia/congregations/cfaith/documents/rc_ddf_doc_20250128_antiqua-et-nova_en.html\",\"verify_status\":\"ok\"},\"quote\":\"Between a machine and a human being, only the latter is truly a moral agent.\",\"quote_label\":\"Antiqua et Nova (2025), par. 39\",\"revision\":0,\"scores\":{\"D1\":0,\"D2\":2,\"D3\":1,\"D4\":2,\"D5\":2,\"D6\":1},\"segment\":\"faith-institution\",\"twilight\":false,\"url\":\"https://www.vatican.va/roman_curia/congregations/cfaith/documents/rc_ddf_doc_20250128_antiqua-et-nova_en.html\"},{\"c2_fit\":\"fits\",\"c3\":\"Both-split\",\"ca\":12,\"coded_date\":\"2026-08-02\",\"id\":\"ala\",\"last_changed\":\"2026-08-02\",\"name\":\"American Library Association\",\"posture\":\"Balanced\",\"provenance\":{\"url\":\"https://www.ala.org/sites/default/files/2026-06/ALA%20CD%2044.2%20AI%20Guidance%20Document%20-%20Final.pdf\",\"verify_status\":\"ok\"},\"quote\":\"AI will complement rather than replace human intelligence, reasoning, deliberation, and critical thinking; humans remain accountable for AI-automated decisions and their consequences.\",\"quote_label\":\"ALA, Guidance on the Use of Artificial Intelligence in Libraries (CD#44.2, adopted 2026 Annual Conference), Public Good \\u2014 Preserving Human Decision-Making\",\"revision\":1,\"scores\":{\"D1\":2,\"D2\":2,\"D3\":2,\"D4\":2,\"D5\":2,\"D6\":2},\"segment\":\"library\",\"twilight\":false,\"url\":\"https://www.ala.org/sites/default/files/2026-06/ALA%20CD%2044.2%20AI%20Guidance%20Document%20-%20Final.pdf\"},{\"c2_fit\":\"partially\",\"c3\":\"Both-split\",\"ca\":8,\"coded_date\":\"2026-07-12\",\"id\":\"qaa-uk\",\"last_changed\":null,\"name\":\"QAA (UK Quality Assurance Agency)\",\"posture\":\"Enabling\",\"provenance\":{\"note\":\"Coded from the flagship advice paper linked off the watchlist resources page. Anti-ban, integration-with-integrity stance: 'This approach is preferable to trying to ban the use of these tools outright.' D2 anchored on student responsibility for submission integrity; D6 on 'the ability to check facts and authenticate information derived from Generative Artificial Intelligence software has emerged as a key graduate attribute'. Hybrid-submission gray zone handled through support systems first (twilight). Permit-vs-reserve line drawn on evidencing use, with verification economics as motivation (detection 'fraught with difficulty' drives assessment redesign) - partial fit.\",\"url\":\"https://www.qaa.ac.uk/sector-resources/generative-artificial-intelligence/qaa-advice-and-resources\",\"verify_status\":\"ok\"},\"quote\":\"Policies should be transparent and clearly communicated to staff and students, emphasising that academic misconduct is unacceptable and that responsibility for the integrity of the submission lies with the student.\",\"quote_label\":\"Maintaining quality and standards in the ChatGPT era (2023-05-08)\",\"revision\":0,\"scores\":{\"D1\":1,\"D2\":2,\"D3\":1,\"D4\":1,\"D5\":1,\"D6\":2},\"segment\":\"gov-education\",\"twilight\":true,\"url\":\"https://www.qaa.ac.uk/sector-resources/generative-artificial-intelligence/qaa-advice-and-resources\"},{\"c2_fit\":\"contradicts\",\"c3\":\"Relational\",\"ca\":9,\"coded_date\":\"2026-07-25\",\"id\":\"wga\",\"last_changed\":null,\"name\":\"Writers Guild of America \\u2014 2023 MBA, AI provisions\",\"posture\":\"Prohibitive\",\"provenance\":{\"url\":\"https://www.wga.org/contracts/know-your-rights/artificial-intelligence\",\"verify_status\":\"ok\"},\"quote\":\"Neither traditional AI (technologies including those used in CGI and VFX) nor generative AI (GAI, meaning artificial intelligence that produces content including written material) is a writer, so no written material produced by traditional AI or GAI can be considered literary material.\",\"quote_label\":\"WGA 2023 Minimum Basic Agreement, AI provisions (Know Your Rights: Artificial Intelligence)\",\"revision\":0,\"scores\":{\"D1\":1,\"D2\":2,\"D3\":2,\"D4\":2,\"D5\":2,\"D6\":0},\"segment\":\"labor-union\",\"twilight\":false,\"url\":\"https://www.wga.org/contracts/know-your-rights/artificial-intelligence\"},{\"c2_fit\":\"contradicts\",\"c3\":\"Neither\",\"ca\":10,\"coded_date\":\"2026-07-25\",\"id\":\"china-cac\",\"last_changed\":null,\"name\":\"Cyberspace Administration of China \\u2014 Interim Measures for Generative AI Services\",\"posture\":\"Balanced\",\"provenance\":{\"url\":\"https://www.cac.gov.cn/2023-07/13/c_1690898327029107.htm\",\"verify_status\":\"ok\"},\"quote\":\"Uphold the Core Socialist Values; content such as that inciting subversion of national sovereignty or the overturn of the socialist system, endangering national security, as well as fake and harmful information, must not be generated\",\"quote_label\":\"CAC, Interim Measures for the Management of Generative AI Services, Art. 4 \\u2014 English rendering per China Law Translate (chinalawtranslate.com/en/generative-ai-interim/); official Chinese text at cac.gov.cn\",\"revision\":0,\"scores\":{\"D1\":2,\"D2\":2,\"D3\":2,\"D4\":2,\"D5\":1,\"D6\":1},\"segment\":\"regulator\",\"twilight\":false,\"url\":\"https://www.cac.gov.cn/2023-07/13/c_1690898327029107.htm\"},{\"c2_fit\":\"contradicts\",\"c3\":\"Neither\",\"ca\":7,\"coded_date\":\"2026-07-26\",\"id\":\"us-copyright-office\",\"last_changed\":null,\"name\":\"U.S. Copyright Office\",\"posture\":\"Balanced\",\"provenance\":{\"note\":\"Disconfirming case retained. Reserves authorship for humans by constitutional and statutory doctrine \\u2014 a machine cannot be an author \\u2014 NOT by verification cost. Verification appears only as a secondary, technology-contingent consideration. Drained from tranche-1-staged-2026-06-23; quote re-fetched live 2026-07-26 and confirmed verbatim. Record URL corrected from the Part 2 Copyrightability Report to the Registration Guidance the quote actually comes from.\",\"url\":\"https://www.copyright.gov/ai/ai_policy_guidance.pdf\",\"verify_status\":\"primary-live-2026-07-26\"},\"quote\":\"Most fundamentally, the term \\u201cauthor,\\u201d which is used in both the Constitution and the Copyright Act, excludes non-humans.\",\"quote_label\":\"Copyright Registration Guidance: Works Containing Material Generated by Artificial Intelligence (88 Fed. Reg. 16190, Mar. 16, 2023), p.1\",\"revision\":0,\"scores\":{\"D1\":1,\"D2\":2,\"D3\":2,\"D4\":1,\"D5\":0,\"D6\":1},\"segment\":\"regulator\",\"twilight\":false,\"url\":\"https://www.copyright.gov/ai/ai_policy_guidance.pdf\"},{\"c2_fit\":\"contradicts\",\"c3\":\"Both-split\",\"ca\":10,\"coded_date\":\"2026-08-16\",\"id\":\"annals-mathematics\",\"last_changed\":\"2026-08-16\",\"name\":\"Annals of Mathematics (Princeton University & IAS)\",\"posture\":\"Balanced\",\"provenance\":{\"note\":\"Verbatim quote corrected 2026-08-16 to match a one-word copyedit in the source (see change history). c2_fit=contradicts is unchanged: mathematics is the cheapest-proof domain in the corpus \\u2014 a proof either checks or it does not \\u2014 yet the Annals reserves authorship for humans absolutely, which is the reverse of what verification economics would predict.\",\"url\":\"https://annals.math.princeton.edu/submission-guidelines\",\"verify_status\":\"primary-live-2026-08-16\"},\"quote\":\"Authors must be human, and they must take full responsibility for the content of the submission, including its correctness and the integrity and accuracy of its citations. AI agents cannot be named authors. If an AI tool or LLM contributed an idea, authors should describe that idea and specify its location in the paper.\",\"quote_label\":\"Annals of Mathematics \\u2014 Submission Guidelines, AI & LLM Policy\",\"revision\":1,\"scores\":{\"D1\":2,\"D2\":2,\"D3\":2,\"D4\":1,\"D5\":2,\"D6\":1},\"segment\":\"publisher\",\"twilight\":false,\"url\":\"https://annals.math.princeton.edu/submission-guidelines\"},{\"c2_fit\":\"fits\",\"c3\":\"Both-split\",\"ca\":10,\"coded_date\":\"2026-08-02\",\"id\":\"uk-judiciary\",\"last_changed\":null,\"name\":\"UK Courts and Tribunals Judiciary \\u2014 AI Guidance for Judicial Office Holders\",\"posture\":\"Balanced\",\"provenance\":{\"url\":\"https://www.judiciary.uk/wp-content/uploads/2025/04/Refreshed-AI-Guidance-published-version.pdf\",\"verify_status\":\"ok\"},\"quote\":\"Judicial office holders are personally responsible for material which is produced in their name.\",\"quote_label\":\"Artificial Intelligence (AI) \\u2014 Guidance for Judicial Office Holders, 14 April 2025, \\u00a76 Take Responsibility\",\"revision\":0,\"scores\":{\"D1\":1,\"D2\":2,\"D3\":1,\"D4\":2,\"D5\":2,\"D6\":2},\"segment\":\"courts-legal\",\"twilight\":false,\"url\":\"https://www.judiciary.uk/wp-content/uploads/2025/04/Refreshed-AI-Guidance-published-version.pdf\"},{\"c2_fit\":\"fits\",\"c3\":\"Both-split\",\"ca\":11,\"coded_date\":\"2026-08-02\",\"id\":\"nhs-england\",\"last_changed\":null,\"name\":\"NHS England \\u2014 AI-enabled ambient scribing guidance\",\"posture\":\"Balanced\",\"provenance\":{\"url\":\"https://www.england.nhs.uk/long-read/guidance-on-the-use-of-ai-enabled-ambient-scribing-products-in-health-and-care-settings/\",\"verify_status\":\"ok\"},\"quote\":\"ensure users review and approve any product outputs prior to further actions\",\"quote_label\":\"NHS England \\u2014 Guidance on the use of AI-enabled ambient scribing products in health and care settings\",\"revision\":0,\"scores\":{\"D1\":2,\"D2\":2,\"D3\":2,\"D4\":1,\"D5\":2,\"D6\":2},\"segment\":\"healthcare-provider\",\"twilight\":false,\"url\":\"https://www.england.nhs.uk/long-read/guidance-on-the-use-of-ai-enabled-ambient-scribing-products-in-health-and-care-settings/\"},{\"c2_fit\":\"fits\",\"c3\":\"Both-split\",\"ca\":11,\"coded_date\":\"2026-08-02\",\"id\":\"calbar\",\"last_changed\":null,\"name\":\"State Bar of California \\u2014 Practical Guidance for Generative AI in the Practice of Law\",\"posture\":\"Balanced\",\"provenance\":{\"url\":\"https://www.calbar.ca.gov/Portals/0/documents/ethics/Generative-AI-Practical-Guidance.pdf\",\"verify_status\":\"ok\"},\"quote\":\"Critically, any use of AI must not diminish or abdicate professional judgment. A lawyer remains fully responsible for any outputs and work product generated with the assistance of AI.\",\"quote_label\":\"State Bar of California COPRAC, Practical Guidance for the Use of Generative AI in the Practice of Law (2026 revision), Conclusion\",\"revision\":0,\"scores\":{\"D1\":2,\"D2\":2,\"D3\":1,\"D4\":2,\"D5\":2,\"D6\":2},\"segment\":\"professional-licensing\",\"twilight\":false,\"url\":\"https://www.calbar.ca.gov/Portals/0/documents/ethics/Generative-AI-Practical-Guidance.pdf\"},{\"c2_fit\":\"fits\",\"c3\":\"Both-split\",\"ca\":10,\"coded_date\":\"2026-08-02\",\"id\":\"esma\",\"last_changed\":null,\"name\":\"ESMA \\u2014 Public Statement on AI in retail investment services\",\"posture\":\"Balanced\",\"provenance\":{\"url\":\"https://www.esma.europa.eu/sites/default/files/2024-05/ESMA35-335435667-5924__Public_Statement_on_AI_and_investment_services.pdf\",\"verify_status\":\"ok\"},\"quote\":\"firms\\u2019 decisions remain the responsibility of management bodies, irrespective of whether those decisions are taken by people or AI-based tools.\",\"quote_label\":\"ESMA Public Statement on the use of AI in the provision of retail investment services (ESMA35-335435667-5924, 30 May 2024), para 2\",\"revision\":0,\"scores\":{\"D1\":2,\"D2\":2,\"D3\":2,\"D4\":1,\"D5\":1,\"D6\":2},\"segment\":\"financial-regulator\",\"twilight\":false,\"url\":\"https://www.esma.europa.eu/sites/default/files/2024-05/ESMA35-335435667-5924__Public_Statement_on_AI_and_investment_services.pdf\"},{\"c2_fit\":\"fits\",\"c3\":\"Both-split\",\"ca\":12,\"coded_date\":\"2026-08-09\",\"id\":\"ama\",\"last_changed\":null,\"name\":\"American Medical Association \\u2014 Augmented Intelligence Development, Deployment, and Use in Health Care\",\"posture\":\"Balanced\",\"provenance\":{\"note\":\"Second load-bearing line, Rec. 2(b): 'AI tools or systems cannot augment, create, or otherwise generate records, communications, or other content on behalf of a physician without that physician's consent and final review.' D4 anchored on Rec. 2(d) ('Where patient-facing content is generated by AI, the use of AI in generating that content should be disclosed or otherwise noted within the content'), Rec. 3(a)(viii)(2) ('Constraint to evidence-based outcomes and mitigation of \\\"hallucination\\\"/\\\"confabulation\\\" or other output error'), and Rec. 8(e) ('requiring the exclusion of AI systems as authors'). Twilight framing is explicit and repeated: 'there is not yet any clear legal standard for determining liability' and 'Given that there are no regulations or generally accepted standards or frameworks to govern the design, development, and deployment of generative AI' \\u2014 precedent collapse; plus AI model drift/degradation and post-market surveillance \\u2014 feedback delay. c2_fit 'fits': the reserve line is drawn by harm potential AND named verification difficulty \\u2014 Rec. 4(b)(i) governs 'lack of ability to readily verify the accuracy of responses or the sources used to generate the response.'\",\"url\":\"https://www.ama-assn.org/system/files/ama-ai-principles.pdf\",\"verify_status\":\"primary-live-2026-08-09\"},\"quote\":\"Clinical decisions influenced by AI must be made with specified qualified human intervention points during the decision-making process. A qualified human is defined as a licensed physician with the necessary qualifications and training to independently provide the same medical service without the aid of AI.\",\"quote_label\":\"Recommendation 1(g), General Governance (November 2024)\",\"revision\":0,\"scores\":{\"D1\":2,\"D2\":2,\"D3\":2,\"D4\":2,\"D5\":2,\"D6\":2},\"segment\":\"medical-association\",\"twilight\":true,\"url\":\"https://www.ama-assn.org/system/files/ama-ai-principles.pdf\"},{\"c2_fit\":\"partially\",\"c3\":\"Evidential\",\"ca\":10,\"coded_date\":\"2026-08-09\",\"id\":\"actuarial-standards-board\",\"last_changed\":null,\"name\":\"Actuarial Standards Board \\u2014 ASOP No. 56 (Modeling)\",\"posture\":\"Enabling\",\"provenance\":{\"note\":\"DISCONFIRMATION PROBE \\u2014 coded as a deviation, not a confirmation. D4 = 0: the standard predates generative AI and carries no fabrication or synthetic-identity provision at all. c2_fit 'partially' because the permit line runs against verification economics in two places: \\u00a73.4 expressly permits reliance on a model where 'the actuary has a limited ability either to obtain information about the model or to understand the underlying workings of the model,' curing it with disclosure rather than reserve; and \\u00a73.6(e) makes 'the balance between the cost of the mitigation efforts and the reduction in potential model risk' a reason to verify LESS, inverting the usual direction. The compensating control is \\u00a73.6.2 Model Output Validation \\u2014 'The actuary should validate that the model output reasonably represents that which is being modeled' \\u2014 tested against historical actual results and hold-out data. Read: an institution can hold accountability firmly on a named human (D2=2) while permitting uninspectable machine judgment on work whose proof is decades out.\",\"url\":\"http://www.actuarialstandardsboard.org/asops/modeling-3/\",\"verify_status\":\"primary-live-2026-08-09\"},\"quote\":\"If preparing documentation, the actuary should prepare such documentation in a form such that another actuary qualified in the same practice area could assess the reasonableness of the actuary's work.\",\"quote_label\":\"ASOP No. 56, Modeling, \\u00a73.7 Documentation (adopted December 2019, effective 2020-10-01)\",\"revision\":0,\"scores\":{\"D1\":2,\"D2\":2,\"D3\":2,\"D4\":0,\"D5\":2,\"D6\":2},\"segment\":\"standards-body\",\"twilight\":false,\"url\":\"http://www.actuarialstandardsboard.org/asops/modeling-3/\"},{\"c2_fit\":\"fits\",\"c3\":\"Evidential\",\"ca\":9,\"coded_date\":\"2026-08-16\",\"id\":\"easa\",\"last_changed\":null,\"name\":\"EASA \\u2014 Concept Paper: Guidance for Level 1&2 Machine Learning Applications\",\"posture\":\"Balanced\",\"provenance\":{\"note\":\"Level 3 AI is explicitly outside this guidance's scope (\\\"covering Level 1 and Level 2 AI applications, but not covering yet Level 3 AI applications\\\"); the end user holds full authority up to Level 2A, with \\\"the ability to intervene and override any decisions taken and/or actions made by the AI-based system.\\\" D2=1 rather than 2 because the ethics 'Accountability' gear is an optional self-assessment item that applicants may record as not applicable, and no provision states that a named human bears responsibility for AI-influenced output. D4=0: synthetic data appears only as a permitted training/test supplement, never as a prohibition. twilight=true on the explicit precedent-collapse framing quoted above plus \\\"we may not always be able to open the 'AI black box' to the extent required and that the associated residual risk may need to be addressed to deal with the inherent uncertainty of AI.\\\"\",\"url\":\"https://www.easa.europa.eu/en/downloads/137631/en\",\"verify_status\":\"primary-live-2026-08-16\"},\"quote\":\"Firstly, learning assurance covers the paradigm shift from programming to learning, as the existing development assurance methods are not adapted to cover learning processes specific to AI/ML.\",\"quote_label\":\"EASA Concept Paper: guidance for Level 1 & 2 machine learning applications, Proposed Issue 02 \\u2014 AI assurance building block\",\"revision\":0,\"scores\":{\"D1\":2,\"D2\":1,\"D3\":2,\"D4\":0,\"D5\":2,\"D6\":2},\"segment\":\"aviation-regulator\",\"twilight\":true,\"url\":\"https://www.easa.europa.eu/en/downloads/137631/en\"},{\"c2_fit\":\"contradicts\",\"c3\":\"Evidential\",\"ca\":10,\"coded_date\":\"2026-08-16\",\"id\":\"naic\",\"last_changed\":null,\"name\":\"NAIC \\u2014 Model Bulletin on the Use of Artificial Intelligence Systems by Insurers\",\"posture\":\"Enabling\",\"provenance\":{\"note\":\"Disconfirmation probe that paid out, replicating the CFPB result in an adjacent industry. Human involvement is a risk-calibration factor, not a requirement: \\u00a73 directs that controls be \\\"commensurate with\\\" the insurer's own risk assessment \\\"considering: ... (iii) the extent to which humans are involved in the final decision-making process.\\\" No provision reserves any decision for a human anywhere across underwriting, rating, claims or fraud detection \\u2014 the basis for D5=1 and c2_fit=contradicts. D4=1 rests on the binding accuracy standard (decisions must not be \\\"inaccurate, arbitrary, capricious, or unfairly discriminatory\\\"), not on any fabrication or synthetic-identity rule, which the bulletin lacks despite defining Generative AI. twilight=false: the bulletin asserts precedent CONTINUITY, insisting existing law applies unchanged.\",\"url\":\"https://content.naic.org/sites/default/files/inline-files/2023-12-4%20Model%20Bulletin_Adopted_0.pdf\",\"verify_status\":\"primary-live-2026-08-16\"},\"quote\":\"Compliance with these standards is required regardless of the tools and methods Insurers use to make such decisions.\",\"quote_label\":\"NAIC Model Bulletin: Use of Artificial Intelligence Systems by Insurers, \\u00a73 (adopted by Executive (EX) Committee and Plenary, 4 December 2023)\",\"revision\":0,\"scores\":{\"D1\":2,\"D2\":2,\"D3\":2,\"D4\":1,\"D5\":1,\"D6\":2},\"segment\":\"insurance-regulator\",\"twilight\":false,\"url\":\"https://content.naic.org/sites/default/files/inline-files/2023-12-4%20Model%20Bulletin_Adopted_0.pdf\"},{\"c2_fit\":\"fits\",\"c3\":\"Both-split\",\"ca\":9,\"coded_date\":\"2026-08-16\",\"id\":\"spc-china\",\"last_changed\":null,\"name\":\"Supreme People's Court of China \\u2014 Opinions on Regulating and Strengthening the Applications of AI in the Judicial Fields (2022)\",\"posture\":\"Enabling\",\"provenance\":{\"note\":\"Disconfirmation probe that did NOT disconfirm \\u2014 the strongest counter-case available, and it failed to break the pattern. The SPC mandates court-wide AI build-out with dated targets for 2025 and 2030 (Arts. 2, 8-12) while imposing the corpus's most absolute human-reserve clause (Art. 5), which also fixes accountability: \\\"all judicial accountability ultimately falls on the decision-maker.\\\" Mandated adoption and absolute reserve are compatible; posture=Enabling with D5=2 is the shape. D4=0: unlike uk-judiciary and nz-courts, which both name the fabricated-citation failure mode, the 2022 Opinions contain no fabrication or hallucination provision even though Art. 8 contemplates \\\"AI-assisted legal documents generation and review.\\\" D3=1: Art. 6 mandates that capabilities and limitations be \\\"instructed and identified in a manner that can be easily understood\\\" at point of use, but nothing requires AI-generated judicial documents to be labelled. c3=Both-split: evidential (Art. 6 interpretability, testability, verifiability) alongside authority-based trust (registration with \\\"relevant authoritative entities,\\\" Judicial AI Ethics Council, Core Socialist Values). Coded from translated-secondary because english.court.gov.cn no longer resolves the 2022 release \\u2014 the same accommodation already made for china-cac.\",\"url\":\"https://www.chinajusticeobserver.com/law/x/the-supreme-people-s-court-the-opinions-on-regulating-and-strengthening-the-applications-of-artificial-intelligence-in-the-judicial-field-20221208\",\"verify_status\":\"translated-secondary-2026-08-16\"},\"quote\":\"AI shall not make judicial decision substituting for the judge in any case, disregarding technology advancement. The results from AI shall be for supplemental references only, for adjudication or judicial supervision and management.\",\"quote_label\":\"Opinions on Regulating and Strengthening the Applications of AI in the Judicial Fields, Art. 5 (Principle of Supporting Adjudication), promulgated 8 December 2022 \\u2014 English translation from the PRC SPC website, reproduced by China Justice Observer\",\"revision\":0,\"scores\":{\"D1\":2,\"D2\":2,\"D3\":1,\"D4\":0,\"D5\":2,\"D6\":2},\"segment\":\"courts-legal\",\"twilight\":false,\"url\":\"https://www.chinajusticeobserver.com/law/x/the-supreme-people-s-court-the-opinions-on-regulating-and-strengthening-the-applications-of-artificial-intelligence-in-the-judicial-field-20221208\"},{\"c2_fit\":\"contradicts\",\"c3\":\"Both-split\",\"ca\":5,\"coded_date\":\"2026-08-16\",\"id\":\"imda-pdpc\",\"last_changed\":null,\"name\":\"IMDA / PDPC Singapore \\u2014 Model AI Governance Framework (2nd edition)\",\"posture\":\"Enabling\",\"provenance\":{\"note\":\"Disconfirmation probe that paid out, and the lowest-scoring regulator in the corpus. The reserve line is drawn on severity x probability of HARM, not on verification economics, and footnote 4(c) makes operational infeasibility an independent permit ground: \\\"having a human-in-the-loop would be unfeasible in high-speed financial trading, and be impractical in the case of driverless vehicles\\\" \\u2014 machine judgment permitted precisely where proof of a correct individual decision is scarce. D1/D6=1 because traceability and auditability are explicitly discretionary and cost-gated: \\\"It may not be feasible or cost-effective to implement even the most essential of these measures for all algorithms,\\\" with reproducibility, traceability and auditability described as \\\"more resource-intensive\\\" and relevant only \\\"in specific scenarios.\\\" c3=Both-split because evidential measures are selected by which \\\"will be most effective in building trust with their stakeholders\\\" \\u2014 evidence in service of relationship. D3=1: all disclosure is \\\"encouraged\\\" or organisations \\\"can consider,\\\" never required. D4=0: no fabrication, deepfake or synthetic-identity provision anywhere (a 2020 pre-generative document). twilight=true on \\\"unlike earlier technologies, some aspects of autonomous predictions or decisions made by AI may not be fully explainable\\\" and \\\"perfect explainability, transparency and fairness are impossible to attain.\\\"\",\"url\":\"https://www.pdpc.gov.sg/-/media/Files/PDPC/PDF-Files/Resource-for-Organisation/AI/SGModelAIGovFramework2.pdf\",\"verify_status\":\"primary-live-2026-08-16\"},\"quote\":\"Human-out-of-the-loop suggests that there is no human oversight over the execution of decisions. The AI system has full control without the option of human override.\",\"quote_label\":\"Model Artificial Intelligence Governance Framework, Second Edition (released 21 January 2020), \\u00a73.14(b)\",\"revision\":0,\"scores\":{\"D1\":1,\"D2\":1,\"D3\":1,\"D4\":0,\"D5\":1,\"D6\":1},\"segment\":\"data-protection-regulator\",\"twilight\":true,\"url\":\"https://www.pdpc.gov.sg/-/media/Files/PDPC/PDF-Files/Resource-for-Organisation/AI/SGModelAIGovFramework2.pdf\"}]"
# --- END GENERATED CORPUS --------------------------------------------------
CORPUS = json.loads(_CORPUS_JSON)


# ----------------------------------------------------------- helpers ----

def _dataset_block(corpus):
    """The provenance stamp that rides on EVERY payload.

    A stale endpoint that announces it is stale is honest; one that answers
    confidently is not. `n` is the size of the corpus that actually answered
    this call, `version` the dataset release it came from, and `live_dataset`
    the URL an agent can fetch to check both without trusting us.
    """
    return {
        "name": DATASET_NAME,
        "version": CORPUS_VERSION or None,
        "n": len(corpus),
        "generated_at": CORPUS_GENERATED_AT,
        "source": _BASE_URL,
        "live_dataset": _BASE_URL + "/index.json",
        "license": "CC-BY-4.0",
    }


def _snapshot_label(corpus):
    """Same facts as one human-readable line, e.g. 'v2026-07-31 (n=59)'."""
    return "v%s (n=%d)" % (CORPUS_VERSION or "unknown", len(corpus))


def _slim(c):
    """Compact record for list/search output."""
    return {
        "id": c.get("id"), "name": c.get("name"), "segment": c.get("segment"),
        "ca": c.get("ca"), "posture": c.get("posture"),
        "c2_fit": c.get("c2_fit"), "c3": c.get("c3"),
        "twilight": bool(c.get("twilight", False)),
    }


def _full(c):
    """Full citable record + permalink."""
    scores = c.get("scores", {})
    prov = c.get("provenance") or {}
    return {
        "id": c.get("id"), "name": c.get("name"), "segment": c.get("segment"),
        "scores": {d: scores.get(d) for d in DIMENSIONS},
        "ca": c.get("ca"), "posture": c.get("posture"),
        "c2_fit": c.get("c2_fit"), "c3": c.get("c3"),
        "twilight": bool(c.get("twilight", False)),
        "quote": c.get("quote"), "quote_label": c.get("quote_label"),
        "source_url": c.get("url"),
        "verify_status": c.get("verify") or prov.get("verify_status", "ok"),
        "permalink": "%s/institutions/%s" % (_BASE_URL, c.get("id")),
        "coded_date": c.get("coded_date"),
        # When this record last MOVED, and how many times it has been re-coded.
        # A verbatim quote is only evidence once you know how old it is.
        "last_changed": c.get("last_changed"),
        "revision": c.get("revision", 0),
    }


def _norm(s):
    return " ".join(str(s or "").strip().lower().split())


def _resolve(corpus, needle):
    """Resolve a name/id to exactly ONE record, or report the tie.

    Returns `(record, candidates)`. A record means unique resolution. No record
    plus a non-empty `candidates` means several institutions match and the
    caller has to choose — "University of Cambridge" and "Cambridge University
    Press" are two institutions with two different scores, and returning
    whichever happens to sit earlier in the file is a confidently wrong answer
    with no ambiguity signal attached.

    Tiers, most specific first: exact id, exact name, name/id prefix, substring
    anywhere. The first tier yielding exactly one record wins; the first
    yielding several is reported as the tie.
    """
    n = _norm(needle)
    if not n:
        return None, []
    tiers = (
        [c for c in corpus if _norm(c.get("id")) == n],
        [c for c in corpus if _norm(c.get("name")) == n],
        [c for c in corpus if _norm(c.get("name")).startswith(n)
         or _norm(c.get("id")).startswith(n)],
        [c for c in corpus if n in _norm(c.get("name")) or n in _norm(c.get("id"))],
    )
    for hits in tiers:
        if len(hits) == 1:
            return hits[0], []
        if len(hits) > 1:
            return None, hits
    return None, []


def _ambiguous(field, needle, candidates):
    return {
        "error": "ambiguous institution %r — %d records match"
                 % (needle, len(candidates)),
        "ambiguous": True,
        "field": field,
        "query": needle,
        "candidates": sorted(
            ({"id": c.get("id"), "name": c.get("name"), "ca": c.get("ca")}
             for c in candidates),
            key=lambda r: str(r["id"])),
        "hint": "call again with one of the ids above",
    }


def _no_match(field, needle):
    return {
        "error": "no institution matching %r" % needle,
        "field": field,
        "query": needle,
        "hint": "try ca_index_search to list ids/names",
    }


def _enum_values(corpus, field):
    """The values this corpus actually carries for a categorical field.

    Derived, never listed, so the validator cannot document one vocabulary
    while the data uses another — which is the whole partial/partially bug in
    one sentence.
    """
    return sorted({str(c.get(field)) for c in corpus if c.get(field)})


# Documented-but-wrong spellings, mapped to what the corpus stores. `partially`
# is canonical: it is what the data, the CSV, the JSON schema and the
# methodology page all say. `partial` shipped only in this endpoint's own tool
# description, so the DOCUMENTATION was the wrong half and is corrected below.
# The alias stays so the records that description made unreachable answer to
# either spelling.
_ALIASES = {
    "c2_fit": {"partial": "partially", "partly": "partially"},
}


# ----------------------------------------------------------- handlers ----

def handle_lookup(corpus, args):
    needle = args.get("institution")
    c, candidates = _resolve(corpus, needle)
    if c is None:
        return (_ambiguous("institution", needle, candidates) if candidates
                else _no_match("institution", needle))
    return _full(c)


def handle_search(corpus, args):
    # Categorical filters are validated against the corpus's own vocabulary. A
    # value that appears nowhere in the data is a query bug, and answering it
    # with `{count: 0}` is the endpoint agreeing with a caller who is wrong.
    wanted = {}
    for arg, field in (("posture", "posture"), ("trust_logic", "c3"),
                       ("c2_fit", "c2_fit")):
        raw = args.get(arg)
        raw = raw.strip() if isinstance(raw, str) else raw
        if not raw:
            continue
        key = _ALIASES.get(arg, {}).get(str(raw).lower(), str(raw).lower())
        valid = _enum_values(corpus, field)
        match = next((v for v in valid if v.lower() == key), None)
        if match is None:
            return {
                "error": "unknown %s value %r" % (arg, raw),
                "field": arg,
                "valid_values": valid,
                "hint": "%s accepts one of: %s" % (arg, ", ".join(valid) or "(none)"),
            }
        wanted[field] = match

    segment = (args.get("segment") or "").strip().lower() or None
    min_ca = args.get("min_ca")
    max_ca = args.get("max_ca")
    twilight = args.get("twilight")
    out = []
    for c in corpus:
        if any(str(c.get(f, "")) != v for f, v in wanted.items()):
            continue
        if segment and segment not in str(c.get("segment", "")).lower():
            continue
        if isinstance(min_ca, (int, float)) and (c.get("ca") is None or c["ca"] < min_ca):
            continue
        if isinstance(max_ca, (int, float)) and (c.get("ca") is None or c["ca"] > max_ca):
            continue
        if isinstance(twilight, bool) and bool(c.get("twilight", False)) != twilight:
            continue
        out.append(_slim(c))
    out.sort(key=lambda r: (-(r["ca"] if r["ca"] is not None else -1), r["name"] or ""))
    return {"count": len(out), "results": out}


def handle_compare(corpus, args):
    resolved, unresolved = {}, []
    for key in ("a", "b"):
        needle = args.get(key)
        rec, candidates = _resolve(corpus, needle)
        if rec is not None:
            resolved[key] = rec
        elif candidates:
            unresolved.append(_ambiguous(key, needle, candidates))
        else:
            unresolved.append(_no_match(key, needle))
    if unresolved:
        return {"error": "could not resolve: %s"
                         % "; ".join(u["error"] for u in unresolved),
                "unresolved": unresolved}
    fa, fb = _full(resolved["a"]), _full(resolved["b"])
    diffs = {d: [fa["scores"][d], fb["scores"][d]]
             for d in DIMENSIONS if fa["scores"][d] != fb["scores"][d]}
    return {"a": fa, "b": fb,
            "ca_gap": (fa["ca"] - fb["ca"]) if (fa["ca"] is not None and fb["ca"] is not None) else None,
            "dimension_diffs": diffs}


def handle_stats(corpus, args):
    cas = [c.get("ca") for c in corpus if isinstance(c.get("ca"), (int, float))]
    by_seg = {}
    for c in corpus:
        by_seg.setdefault(c.get("segment", "?"), []).append(c.get("ca"))
    seg_means = {s: round(sum(v) / len(v), 1)
                 for s, v in by_seg.items() if v and all(isinstance(x, (int, float)) for x in v)}
    fit_counts = {}
    for c in corpus:
        fit_counts[c.get("c2_fit", "?")] = fit_counts.get(c.get("c2_fit", "?"), 0) + 1
    logic_counts = {}
    for c in corpus:
        logic_counts[c.get("c3", "?")] = logic_counts.get(c.get("c3", "?"), 0) + 1
    return {
        "n": len(corpus),
        "mean_ca": round(sum(cas) / len(cas), 1) if cas else None,
        "ca_range": [min(cas), max(cas)] if cas else None,
        "by_segment_mean_ca": seg_means,
        "c2_fit_counts": fit_counts,
        "trust_logic_counts": logic_counts,
        "twilight_count": sum(1 for c in corpus if c.get("twilight")),
        "source": _BASE_URL,
        "corpus_snapshot": _snapshot_label(corpus),
    }


def handle_methodology(corpus, args):
    return {
        "instrument": {
            "scale": "0-12 composite (six dimensions, 0-2 each)",
            "dimensions": [{"key": d, "label": DIM_LABELS[d]} for d in DIMENSIONS],
            "fields": {
                "ca": "Composite Calibrated Authority score, sum of D1-D6 (0-12).",
                "posture": "Prohibitive | Balanced | Enabling.",
                "c2_fit": "Verification-boundary fit (fits | partially | contradicts).",
                "c3": "Trust-logic: Evidential | Relational | Both-split | Neither.",
                "twilight": "Uses precedent-collapse / feedback-delay / exponential-fog framing.",
            },
        },
        "how_to_cite": "Reitz, C.H. The Calibrated Authority Index. " + _BASE_URL,
        "license": "CC-BY-4.0",
        "methodology_url": _BASE_URL + "/methodology",
        "manifest_url": _BASE_URL + "/institutions/index.json",
        "engine_version": ENGINE_VERSION,
        "corpus_snapshot": _snapshot_label(corpus),
    }


TOOLS = [
    {
        "name": "ca_index_lookup",
        "description": "Look up one institution's Calibrated Authority record by name or id "
                       "(e.g. 'Nature', 'educause'). Returns the six scores, composite CA, "
                       "trust-logic, the verbatim policy quote, source URL, and permalink. "
                       "A name matching several institutions returns the candidates rather "
                       "than guessing one.",
        "inputSchema": {
            "type": "object",
            "properties": {"institution": {"type": "string",
                           "description": "Institution name or id. Exact id wins; an "
                                          "ambiguous name is reported, not guessed."}},
            "required": ["institution"],
        },
        "handler": handle_lookup,
    },
    {
        "name": "ca_index_search",
        "description": "Filter the index. Any combination of posture (Prohibitive|Balanced|Enabling), "
                       "trust_logic (Evidential|Relational|Both-split|Neither), c2_fit "
                       "(fits|partially|contradicts), segment substring, min_ca/max_ca (0-12), "
                       "twilight (bool). Returns matching institutions sorted by CA. A "
                       "categorical value the corpus does not use is an error listing the "
                       "values it does use, not an empty result.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "posture": {"type": "string",
                            "description": "Prohibitive | Balanced | Enabling."},
                "trust_logic": {"type": "string",
                                "description": "Evidential | Relational | Both-split | Neither."},
                "c2_fit": {"type": "string",
                           "description": "Verification-boundary fit: fits | partially | "
                                          "contradicts. 'partial' is accepted as an alias "
                                          "for 'partially'."},
                "segment": {"type": "string",
                            "description": "Substring match on the institution's segment."},
                "min_ca": {"type": "number"},
                "max_ca": {"type": "number"},
                "twilight": {"type": "boolean"},
            },
        },
        "handler": handle_search,
    },
    {
        "name": "ca_index_compare",
        "description": "Compare two institutions side by side — full records, the CA gap, and "
                       "which of the six dimensions differ. An ambiguous name on either side "
                       "returns that side's candidates.",
        "inputSchema": {
            "type": "object",
            "properties": {"a": {"type": "string"}, "b": {"type": "string"}},
            "required": ["a", "b"],
        },
        "handler": handle_compare,
    },
    {
        "name": "ca_index_stats",
        "description": "Summary statistics for the whole index: N, mean CA, range, per-segment "
                       "means, verification-boundary-fit counts, trust-logic counts, twilight count.",
        "inputSchema": {"type": "object", "properties": {}},
        "handler": handle_stats,
    },
    {
        "name": "ca_index_methodology",
        "description": "The instrument definition (six dimensions + categoricals), how to cite, "
                       "license, and machine-readable manifest URL.",
        "inputSchema": {"type": "object", "properties": {}},
        "handler": handle_methodology,
    },
]

_HANDLERS = {t["name"]: t["handler"] for t in TOOLS}


def _tools_list_payload():
    return [{k: t[k] for k in ("name", "description", "inputSchema")} for t in TOOLS]


def _log_hit(tool, status):
    """Per-tool hit log for the hosted MCP endpoint. The function is stateless,
    so this stdout line IS the counter surface: Vercel captures it into
    Observability/logs — filter on the 'ca-mcp-hit' prefix to count queries and
    see which of the 5 tools agents actually call. Durable running totals would
    need a KV/Edge-Config store (follow-up); this gives per-call granularity now."""
    try:
        print("ca-mcp-hit " + json.dumps({"tool": tool, "status": status}), flush=True)
    except Exception:
        pass


def _stamp(result, corpus):
    """Attach the dataset provenance block to one payload."""
    if isinstance(result, dict):
        result.setdefault("dataset", _dataset_block(corpus))
    return result


def dispatch_tool(name, args, corpus=None):
    """Run a tool by name. Returns (result, is_error).

    One choke point, so the `dataset` stamp cannot be forgotten on a single
    tool the way `corpus_snapshot` was carried by `stats` alone — errors and
    later-added tools included.
    """
    if corpus is None:
        corpus = CORPUS
    if name not in _HANDLERS:
        _log_hit(name, "unknown-tool")
        return _stamp({"error": "unknown tool %r" % name}, corpus), True
    try:
        result = _HANDLERS[name](corpus, args or {})
        is_error = isinstance(result, dict) and "error" in result
        _log_hit(name, "error" if is_error else "ok")
        return _stamp(result, corpus), is_error
    except Exception as e:  # defensive
        _log_hit(name, "exception")
        return _stamp({"error": "%s: %s" % (type(e).__name__, e)}, corpus), True


# ------------------------------------------------------------ JSON-RPC ----

def _ok(mid, result):
    return {"jsonrpc": "2.0", "id": mid, "result": result}


def _err(mid, code, message):
    return {"jsonrpc": "2.0", "id": mid, "error": {"code": code, "message": message}}


def handle_message(msg):
    """Map one JSON-RPC request to a response dict, or None for notifications."""
    if not isinstance(msg, dict):
        return _err(None, -32600, "invalid request")
    method = msg.get("method")
    mid = msg.get("id")
    if method == "initialize":
        params = msg.get("params") or {}
        req = params.get("protocolVersion")
        pv = req if req in SUPPORTED_PROTOCOLS else PROTOCOL_DEFAULT
        return _ok(mid, {
            "protocolVersion": pv,
            "capabilities": {"tools": {}},
            "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
            # Named at the handshake, so a client knows which dataset it is
            # talking to before it calls anything.
            "instructions": (
                "%s, dataset %s. Every tool result carries a `dataset` block "
                "with that version and size; the live dataset is %s/index.json."
                % (DATASET_NAME, _snapshot_label(CORPUS), _BASE_URL)),
        })
    if method in ("notifications/initialized", "initialized") or (
            isinstance(method, str) and method.startswith("notifications/")):
        return None  # notification, no reply
    if method == "ping":
        return _ok(mid, {})
    if method == "tools/list":
        return _ok(mid, {"tools": _tools_list_payload()})
    if method == "tools/call":
        params = msg.get("params") or {}
        result, is_error = dispatch_tool(params.get("name"), params.get("arguments"))
        return _ok(mid, {
            "content": [{"type": "text",
                         "text": json.dumps(result, indent=2, ensure_ascii=False)}],
            "isError": is_error,
        })
    if mid is not None:
        return _err(mid, -32601, "method not found: %s" % method)
    return None


def process_body(raw):
    """One HTTP POST body -> (http_status, json_payload_or_None)."""
    try:
        msg = json.loads(raw.decode("utf-8") if isinstance(raw, bytes) else raw)
    except Exception:
        return 400, _err(None, -32700, "parse error: body is not valid JSON")
    if isinstance(msg, list):  # JSON-RPC batch (2025-03-26 transport)
        if not msg:
            return 400, _err(None, -32600, "invalid request: empty batch")
        responses = [r for r in (handle_message(m) for m in msg) if r is not None]
        if not responses:
            return 202, None  # all notifications
        return 200, responses
    if isinstance(msg, dict):
        resp = handle_message(msg)
        if resp is None:
            return 202, None  # notification
        return 200, resp
    return 400, _err(None, -32600, "invalid request")


# ------------------------------------------------------- Vercel handler ----

class handler(BaseHTTPRequestHandler):

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, DELETE")
        self.send_header("Access-Control-Allow-Headers",
                         "Content-Type, Accept, Authorization, "
                         "Mcp-Session-Id, MCP-Protocol-Version, Last-Event-ID")
        self.send_header("Access-Control-Max-Age", "86400")

    def _send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self._cors()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except (TypeError, ValueError):
            length = 0
        raw = self.rfile.read(length) if length > 0 else b""
        status, payload = process_body(raw)
        if payload is None:
            self.send_response(status)
            self._cors()
            self.send_header("Content-Length", "0")
            self.end_headers()
        else:
            self._send_json(status, payload)

    def do_GET(self):
        # Stateless plain-JSON mode: no server-initiated SSE stream on offer.
        # Per the Streamable HTTP spec a server that does not support the GET
        # stream returns 405. Include a hint for humans poking the URL.
        self._send_json(405, {
            "error": "method not allowed",
            "hint": "This is an MCP Streamable HTTP endpoint. "
                    "POST JSON-RPC (initialize / tools/list / tools/call) here.",
            "connect": "claude mcp add --transport http ca-index " + _BASE_URL + "/api/mcp",
            "dataset": _dataset_block(CORPUS),
        })

    def do_DELETE(self):
        # Stateless server: no sessions to terminate.
        self._send_json(405, {"error": "method not allowed (stateless server, no sessions)"})
