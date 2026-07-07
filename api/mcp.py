"""MCP Streamable HTTP endpoint for the Calibrated Authority Index.

POST /api/mcp — JSON-RPC 2.0 over HTTP per the MCP Streamable HTTP transport
(plain-JSON response mode; no SSE stream — stateless serverless). Methods:
initialize / tools/list / tools/call / ping. Notifications get HTTP 202.

Tool handlers are ported from the local stdio server
(~/.local/lib/ca_index_mcp/server.py) — same transport-agnostic logic, backed
by a bundled snapshot of the public corpus (the N=51 launch freeze) instead of
the live store. Stdlib-only; Vercel Python runtime.

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
CORPUS_SNAPSHOT = "launch freeze v2026-06-22 (N=51)"

DIMENSIONS = ["D1", "D2", "D3", "D4", "D5", "D6"]
DIM_LABELS = {
    "D1": "Traceability & inspectability",
    "D2": "Human authorship & accountability",
    "D3": "Disclosure & labeling",
    "D4": "Synthetic-identity / fabrication prohibition",
    "D5": "Human validation in loop",
    "D6": "Evidential-trust emphasis",
}

# Frozen public corpus snapshot (same 51 records as the launch dataset,
# ca-index export --public v2026-06-22). Regenerate deliberately, never live.
_CORPUS_JSON = '[{"c2_fit":"fits","c3":"Both-split","ca":12,"coded_date":"2026-06-22","id":"uf-cpic","name":"UF Center for Public Interest Communications","posture":"Prohibitive","provenance":{"url":"https://realgoodcenter.jou.ufl.edu/about/ai/","verify_status":"ok"},"quote":"All content must be replicable, evidence-based and traceable to sources that a human researcher can locate, review and re-create.","quote_label":"AI use policy","scores":{"D1":2,"D2":2,"D3":2,"D4":2,"D5":2,"D6":2},"segment":"research-center","twilight":true,"url":"https://realgoodcenter.jou.ufl.edu/about/ai/"},{"c2_fit":"fits","c3":"Both-split","ca":12,"coded_date":"2026-06-22","id":"springer-nature","name":"Springer Nature / Nature","posture":"Prohibitive","provenance":{"url":"https://www.nature.com/nature-portfolio/editorial-policies/ai","verify_status":"ok"},"quote":"An attribution of authorship carries with it accountability for the work, which cannot be effectively applied to LLMs.","quote_label":"Nature Portfolio AI policy","scores":{"D1":2,"D2":2,"D3":2,"D4":2,"D5":2,"D6":2},"segment":"publisher","twilight":true,"url":"https://www.nature.com/nature-portfolio/editorial-policies/ai"},{"c2_fit":"fits","c3":"Both-split","ca":12,"coded_date":"2026-06-22","id":"elsevier","name":"Elsevier","posture":"Balanced","provenance":{"url":"https://www.elsevier.com/about/policies-and-standards/the-use-of-generative-ai-and-ai-assisted-technologies-in-writing-for-elsevier","verify_status":"ok"},"quote":"Authorship implies responsibilities and tasks that can only be attributed to and performed by humans.","quote_label":"Author AI policy","scores":{"D1":2,"D2":2,"D3":2,"D4":2,"D5":2,"D6":2},"segment":"publisher","twilight":false,"url":"https://www.elsevier.com/about/policies-and-standards/the-use-of-generative-ai-and-ai-assisted-technologies-in-writing-for-elsevier"},{"c2_fit":"fits","c3":"Both-split","ca":12,"coded_date":"2026-06-22","id":"wiley","name":"Wiley","posture":"Enabling","provenance":{"url":"https://onlinelibrary.wiley.com/pb-assets/assets/15405885/Generative%20AI%20Policy_September%202023-1695231878293.pdf","verify_status":"primary-verified-2026-06-22"},"quote":"The author is fully responsible for the accuracy of any information provided by the AI Technology.","quote_label":"Generative AI policy","scores":{"D1":2,"D2":2,"D3":2,"D4":2,"D5":2,"D6":2},"segment":"publisher","twilight":true,"url":"https://onlinelibrary.wiley.com/pb-assets/assets/15405885/Generative%20AI%20Policy_September%202023-1695231878293.pdf"},{"c2_fit":"fits","c3":"Both-split","ca":12,"coded_date":"2026-06-22","id":"taylor-francis","name":"Taylor & Francis","posture":"Enabling","provenance":{"url":"https://taylorandfrancis.com/our-policies/ai-policy/","verify_status":"primary-verified-2026-06-22"},"quote":"Generative AI tools must not be listed as an author because such tools are unable to assume responsibility for the submitted content or manage copyright and licensing agreements. These are uniquely human responsibilities that cannot be undertaken by Generative AI tools.","quote_label":"AI policy (browser-verified 2026-06-22)","scores":{"D1":2,"D2":2,"D3":2,"D4":2,"D5":2,"D6":2},"segment":"publisher","twilight":true,"url":"https://taylorandfrancis.com/our-policies/ai-policy/"},{"c2_fit":"fits","c3":"Both-split","ca":10,"coded_date":"2026-06-22","id":"science-aaas","name":"Science / AAAS","posture":"Balanced","provenance":{"url":"https://www.science.org/content/page/science-journals-editorial-policies","verify_status":"secondary-blocked"},"quote":"An AI program cannot be an author of a Science journal paper.","quote_label":"Editorial policy","scores":{"D1":1,"D2":2,"D3":2,"D4":2,"D5":2,"D6":1},"segment":"publisher","twilight":false,"url":"https://www.science.org/content/page/science-journals-editorial-policies"},{"c2_fit":"fits","c3":"Both-split","ca":12,"coded_date":"2026-06-22","id":"icmje","name":"ICMJE","posture":"Balanced","provenance":{"url":"https://www.icmje.org/recommendations/browse/roles-and-responsibilities/defining-the-role-of-authors-and-contributors.html","verify_status":"ok"},"quote":"Chatbots (such as ChatGPT) should not be listed as authors because they cannot be responsible for the accuracy, integrity, and originality of the work, and these responsibilities are required for authorship.","quote_label":"Recommendations — AI by authors","scores":{"D1":2,"D2":2,"D3":2,"D4":2,"D5":2,"D6":2},"segment":"med-integrity","twilight":false,"url":"https://www.icmje.org/recommendations/browse/roles-and-responsibilities/defining-the-role-of-authors-and-contributors.html"},{"c2_fit":"fits","c3":"Relational","ca":7,"coded_date":"2026-06-22","id":"cope","name":"COPE","posture":"Balanced","provenance":{"url":"https://publicationethics.org/guidance/cope-position/authorship-and-ai-tools","verify_status":"ok"},"quote":"AI tools cannot meet the requirements for authorship as they cannot take responsibility for the submitted work. As non-legal entities, they cannot assert the presence or absence of conflicts of interest nor manage copyright and license agreements.","quote_label":"Position: Authorship and AI tools","scores":{"D1":1,"D2":2,"D3":2,"D4":0,"D5":1,"D6":1},"segment":"pub-ethics","twilight":false,"url":"https://publicationethics.org/guidance/cope-position/authorship-and-ai-tools"},{"c2_fit":"fits","c3":"Evidential","ca":12,"coded_date":"2026-06-22","id":"plos","name":"PLOS","posture":"Balanced","provenance":{"url":"https://journals.plos.org/plosone/s/ethical-publishing-practice","verify_status":"primary-verified-2026-06-22"},"quote":"The use of AI tools and technologies to fabricate or otherwise misrepresent primary research data is unacceptable.","quote_label":"Ethical publishing practice (browser-verified)","scores":{"D1":2,"D2":2,"D3":2,"D4":2,"D5":2,"D6":2},"segment":"publisher","twilight":false,"url":"https://journals.plos.org/plosone/s/ethical-publishing-practice"},{"c2_fit":"fits","c3":"Evidential","ca":11,"coded_date":"2026-06-22","id":"poynter","name":"Poynter Institute","posture":"Balanced","provenance":{"url":"https://www.poynter.org/ai-ethics-journalism/ai-ethics-guidelines/","verify_status":"ok"},"quote":"All information generated by AI requires human verification. Everything we publish will live up to our long-time standards of verification.","quote_label":"AI ethics guidelines","scores":{"D1":2,"D2":1,"D3":2,"D4":2,"D5":2,"D6":2},"segment":"journalism","twilight":true,"url":"https://www.poynter.org/ai-ethics-journalism/ai-ethics-guidelines/"},{"c2_fit":"partially","c3":"Both-split","ca":5,"coded_date":"2026-06-22","id":"reuters-institute","name":"Reuters Institute (Oxford)","posture":"Balanced","provenance":{"url":"https://reutersinstitute.politics.ox.ac.uk/generative-ai-and-news-report-2025-how-people-think-about-ais-role-journalism-and-society","verify_status":"ok"},"quote":"You cannot simply \'hack\' your way to trust.","quote_label":"Generative AI and news report 2025","scores":{"D1":1,"D2":1,"D3":1,"D4":0,"D5":1,"D6":1},"segment":"journalism-research","twilight":true,"url":"https://reutersinstitute.politics.ox.ac.uk/generative-ai-and-news-report-2025-how-people-think-about-ais-role-journalism-and-society"},{"c2_fit":"fits","c3":"Both-split","ca":8,"coded_date":"2026-06-22","id":"columbia-tow","name":"Columbia / Tow Center","posture":"Balanced","provenance":{"url":"https://journalism.columbia.edu/CJS2030/AI","verify_status":"ok"},"quote":"We won\'t publish a story if our only source is AI — it\'s not a substitute for the careful review of journalists.","quote_label":"Tow Center / CJR","scores":{"D1":1,"D2":2,"D3":1,"D4":1,"D5":2,"D6":1},"segment":"journalism-research","twilight":true,"url":"https://journalism.columbia.edu/CJS2030/AI"},{"c2_fit":"fits","c3":"Evidential","ca":10,"coded_date":"2026-06-22","id":"ap","name":"Associated Press","posture":"Balanced","provenance":{"url":"https://ds.svcs.associatedpress.com/standards-around-generative-ai","verify_status":"secondary-blocked"},"quote":"Any output from a generative AI tool should be treated as unvetted source material.","quote_label":"Standards around generative AI (via Poynter/Globe reprint)","scores":{"D1":1,"D2":2,"D3":1,"D4":2,"D5":2,"D6":2},"segment":"journalism","twilight":false,"url":"https://ds.svcs.associatedpress.com/standards-around-generative-ai"},{"c2_fit":"fits","c3":"Evidential","ca":8,"coded_date":"2026-06-22","id":"harvard","name":"Harvard University","posture":"Balanced","provenance":{"url":"https://provost.harvard.edu/guidelines-using-chatgpt-and-other-generative-ai-tools-harvard","verify_status":"ok"},"quote":"You are responsible for any content that you produce or publish that includes AI-generated material.","quote_label":"Generative AI guidelines","scores":{"D1":1,"D2":2,"D3":1,"D4":1,"D5":2,"D6":1},"segment":"university","twilight":true,"url":"https://provost.harvard.edu/guidelines-using-chatgpt-and-other-generative-ai-tools-harvard"},{"c2_fit":"fits","c3":"Both-split","ca":9,"coded_date":"2026-06-22","id":"stanford","name":"Stanford University","posture":"Balanced","provenance":{"url":"https://communitystandards.stanford.edu/policies-guidance","verify_status":"ok"},"quote":"Absent a clear statement from a course instructor, use of or consultation with generative AI shall be treated analogously to assistance from another person.","quote_label":"Office of Community Standards","scores":{"D1":1,"D2":2,"D3":2,"D4":1,"D5":1,"D6":2},"segment":"university","twilight":true,"url":"https://communitystandards.stanford.edu/policies-guidance"},{"c2_fit":"fits","c3":"Evidential","ca":8,"coded_date":"2026-06-22","id":"mit","name":"MIT","posture":"Balanced","provenance":{"url":"https://ist.mit.edu/ai-guidance","verify_status":"ok"},"quote":"You are responsible for the accuracy of any information you publish, including AI-generated content.","quote_label":"IS&T AI guidance","scores":{"D1":1,"D2":2,"D3":2,"D4":1,"D5":1,"D6":1},"segment":"university","twilight":true,"url":"https://ist.mit.edu/ai-guidance"},{"c2_fit":"fits","c3":"Evidential","ca":10,"coded_date":"2026-06-22","id":"umich","name":"University of Michigan","posture":"Enabling","provenance":{"url":"https://genai.umich.edu/resources/faculty/course-policies","verify_status":"ok"},"quote":"All data shared with U-M\'s AI services is private and will not be used to train AI models.","quote_label":"ITS AI services","scores":{"D1":2,"D2":2,"D3":1,"D4":1,"D5":2,"D6":2},"segment":"university","twilight":true,"url":"https://genai.umich.edu/resources/faculty/course-policies"},{"c2_fit":"partially","c3":"Evidential","ca":7,"coded_date":"2026-06-22","id":"russell-group","name":"Russell Group (UK)","posture":"Enabling","provenance":{"url":"https://www.russellgroup.ac.uk/policy/policy-briefings/principles-use-generative-ai-tools-education","verify_status":"ok"},"quote":"Accountability for the accuracy of information generated by these tools when transferred to another context lies with the user.","quote_label":"Principles on generative AI in education","scores":{"D1":1,"D2":1,"D3":1,"D4":1,"D5":1,"D6":2},"segment":"university-consortium","twilight":false,"url":"https://www.russellgroup.ac.uk/policy/policy-briefings/principles-use-generative-ai-tools-education"},{"c2_fit":"fits","c3":"Both-split","ca":10,"coded_date":"2026-06-22","id":"mla-cccc","name":"MLA-CCCC Task Force","posture":"Balanced","provenance":{"url":"https://aiandwriting.hcommons.org/working-paper-1/","verify_status":"ok"},"quote":"We and others would caution against using LLMs to assess student writing or to write tailored feedback to students, given the danger of undermining trust and human connection in the classroom.","quote_label":"Joint Task Force, Working Paper 3","scores":{"D1":2,"D2":2,"D3":2,"D4":1,"D5":2,"D6":1},"segment":"education","twilight":false,"url":"https://aiandwriting.hcommons.org/working-paper-1/"},{"c2_fit":"fits","c3":"Both-split","ca":11,"coded_date":"2026-06-22","id":"acm","name":"ACM","posture":"Balanced","provenance":{"note":"Policy updated 2026-05-14: AI writing-assistance disclosure no longer required (research-use still must be described in Methods). D3 2->1; CA 10->11.","url":"https://www.acm.org/publications/policies/new-acm-policy-on-authorship","verify_status":"primary-verified-2026-06-22"},"quote":"When using Artificial Intelligence to assist with writing an ACM submission, ACM no longer requires the disclosure of information regarding the use of AI.","quote_label":"Policy on Authorship, updated 2026-05-14 (browser-verified)","scores":{"D1":2,"D2":2,"D3":1,"D4":2,"D5":2,"D6":2},"segment":"computing-society","twilight":false,"url":"https://www.acm.org/publications/policies/new-acm-policy-on-authorship"},{"c2_fit":"fits","c3":"Both-split","ca":11,"coded_date":"2026-06-22","id":"apa","name":"APA","posture":"Balanced","provenance":{"url":"https://www.apa.org/pubs/journals/resources/publishing-tips/policy-generative-ai","verify_status":"ok"},"quote":"AI is not a conscious human who can consent to the duties and responsibilities of authorship, which include responsibility for post publication changes such as corrections or retractions.","quote_label":"Journals generative-AI policy","scores":{"D1":2,"D2":2,"D3":2,"D4":2,"D5":2,"D6":1},"segment":"society-publisher","twilight":false,"url":"https://www.apa.org/pubs/journals/resources/publishing-tips/policy-generative-ai"},{"c2_fit":"fits","c3":"Both-split","ca":9,"coded_date":"2026-06-22","id":"yale","name":"Yale University","posture":"Balanced","provenance":{"url":"https://provost.yale.edu/news/guidelines-use-generative-ai-tools","verify_status":"ok"},"quote":"Always review and verify outputs generated by AI tools, especially before publication. We are each responsible for the content of our work product.","quote_label":"Provost guidelines","scores":{"D1":1,"D2":2,"D3":2,"D4":1,"D5":2,"D6":1},"segment":"university","twilight":false,"url":"https://provost.yale.edu/news/guidelines-use-generative-ai-tools"},{"c2_fit":"fits","c3":"Both-split","ca":11,"coded_date":"2026-06-22","id":"princeton","name":"Princeton University","posture":"Balanced","provenance":{"url":"https://rrr.princeton.edu/students-and-university/24-academic-regulations","verify_status":"ok"},"quote":"Generative AI is not a source as defined in this provision because its output is not created by a person.","quote_label":"Rights, Rules, Responsibilities 2.4.7","scores":{"D1":2,"D2":2,"D3":2,"D4":2,"D5":1,"D6":2},"segment":"university","twilight":false,"url":"https://rrr.princeton.edu/students-and-university/24-academic-regulations"},{"c2_fit":"partially","c3":"Evidential","ca":6,"coded_date":"2026-06-22","id":"uc-berkeley","name":"University of California, Berkeley","posture":"Balanced","provenance":{"url":"https://oercs.berkeley.edu/appropriate-use-generative-ai-tools","verify_status":"ok"},"quote":"No personal, confidential, proprietary, or otherwise sensitive information may be entered into or generated as output from models.","quote_label":"Appropriate use of generative AI","scores":{"D1":1,"D2":1,"D3":1,"D4":1,"D5":1,"D6":1},"segment":"university","twilight":false,"url":"https://oercs.berkeley.edu/appropriate-use-generative-ai-tools"},{"c2_fit":"fits","c3":"Both-split","ca":8,"coded_date":"2026-06-22","id":"cornell","name":"Cornell University","posture":"Enabling","provenance":{"url":"https://it.cornell.edu/ai/ai-guidelines","verify_status":"ok"},"quote":"You are accountable for your work, regardless of the tools you use to produce it.","quote_label":"AI guidelines","scores":{"D1":1,"D2":2,"D3":1,"D4":1,"D5":2,"D6":1},"segment":"university","twilight":false,"url":"https://it.cornell.edu/ai/ai-guidelines"},{"c2_fit":"fits","c3":"Both-split","ca":11,"coded_date":"2026-06-22","id":"carnegie-mellon","name":"Carnegie Mellon University","posture":"Prohibitive","provenance":{"url":"https://www.cmu.edu/teaching/technology/aitools/academicintegrity/index.html","verify_status":"ok"},"quote":"You are ultimately responsible for the content that you submit.","quote_label":"Eberly Center course-policy examples","scores":{"D1":2,"D2":2,"D3":2,"D4":1,"D5":2,"D6":2},"segment":"university","twilight":false,"url":"https://www.cmu.edu/teaching/technology/aitools/academicintegrity/index.html"},{"c2_fit":"fits","c3":"Evidential","ca":12,"coded_date":"2026-06-22","id":"georgia-tech","name":"Georgia Institute of Technology","posture":"Enabling","provenance":{"url":"https://provost.gatech.edu/sites/default/files/2025-10/AI%20Policy_draft_10.14.2025%202.pdf","verify_status":"ok"},"quote":"Core scholarly and research contributions are expected to remain under the full direction and responsibility of the GT community member.","quote_label":"AI Policy (draft, 2025-10-14)","scores":{"D1":2,"D2":2,"D3":2,"D4":2,"D5":2,"D6":2},"segment":"university","twilight":true,"url":"https://provost.gatech.edu/sites/default/files/2025-10/AI%20Policy_draft_10.14.2025%202.pdf"},{"c2_fit":"fits","c3":"Evidential","ca":11,"coded_date":"2026-06-22","id":"u-toronto","name":"University of Toronto","posture":"Balanced","provenance":{"url":"https://www.viceprovostundergrad.utoronto.ca/wp-content/uploads/2024/08/Syllabus-language-for-Gen-AI-2024-08-21.pdf","verify_status":"ok"},"quote":"Generative AI tools do not meet the criteria for authorship of scholarly works, because these tools cannot take responsibility or be held accountable for submitted work.","quote_label":"SGS guidance","scores":{"D1":2,"D2":2,"D3":2,"D4":1,"D5":2,"D6":2},"segment":"university","twilight":true,"url":"https://www.viceprovostundergrad.utoronto.ca/wp-content/uploads/2024/08/Syllabus-language-for-Gen-AI-2024-08-21.pdf"},{"c2_fit":"fits","c3":"Both-split","ca":9,"coded_date":"2026-06-22","id":"cambridge","name":"University of Cambridge","posture":"Balanced","provenance":{"url":"https://www.educationalpolicy.admin.cam.ac.uk/plagiarism-and-academic-misconduct/artificial-intelligence-ai","verify_status":"ok"},"quote":"A student using any unacknowledged content generated by artificial intelligence within a summative assessment as though it is their own work constitutes academic misconduct.","quote_label":"AI and academic misconduct","scores":{"D1":1,"D2":2,"D3":2,"D4":1,"D5":2,"D6":1},"segment":"university","twilight":true,"url":"https://www.educationalpolicy.admin.cam.ac.uk/plagiarism-and-academic-misconduct/artificial-intelligence-ai"},{"c2_fit":"fits","c3":"Both-split","ca":9,"coded_date":"2026-06-22","id":"ucl","name":"University College London","posture":"Enabling","provenance":{"url":"https://www.ucl.ac.uk/teaching-learning/generative-ai-hub/three-categories-genai-use-assessment","verify_status":"ok"},"quote":"The student should still be the author of their own work — GenAI should be limited to supporting and assisting the student.","quote_label":"Generative AI hub","scores":{"D1":1,"D2":2,"D3":2,"D4":1,"D5":2,"D6":1},"segment":"university","twilight":true,"url":"https://www.ucl.ac.uk/teaching-learning/generative-ai-hub/three-categories-genai-use-assessment"},{"c2_fit":"fits","c3":"Both-split","ca":8,"coded_date":"2026-06-22","id":"asu","name":"Arizona State University","posture":"Balanced","provenance":{"url":"https://tlc.sols.asu.edu/teaching/toolkits/syllabus-and-policies-generative-ai","verify_status":"ok"},"quote":"Any submitted course assignment that does not explicitly articulate how generative AI was used will be assumed to have been created entirely without its use.","quote_label":"Syllabus & policies on generative AI","scores":{"D1":1,"D2":2,"D3":2,"D4":0,"D5":2,"D6":1},"segment":"university","twilight":true,"url":"https://tlc.sols.asu.edu/teaching/toolkits/syllabus-and-policies-generative-ai"},{"c2_fit":"fits","c3":"Both-split","ca":9,"coded_date":"2026-06-22","id":"cambridge-up","name":"Cambridge University Press","posture":"Balanced","provenance":{"url":"https://www.cambridge.org/core/services/publishing-ethics/authorship-and-contributorship-journals","verify_status":"ok"},"quote":"AI does not meet the Cambridge requirements for authorship, given the need for accountability.","quote_label":"Authorship and contributorship policy","scores":{"D1":1,"D2":2,"D3":2,"D4":1,"D5":2,"D6":1},"segment":"publisher","twilight":false,"url":"https://www.cambridge.org/core/services/publishing-ethics/authorship-and-contributorship-journals"},{"c2_fit":"fits","c3":"Evidential","ca":12,"coded_date":"2026-06-22","id":"oxford-up","name":"Oxford University Press","posture":"Balanced","provenance":{"url":"https://academic.oup.com/pages/for-authors/books/author-use-of-artificial-intelligence","verify_status":"ok"},"quote":"Gen AI does not qualify as an author and should not be used to undertake primary authorial responsibilities, such as generating arguments and scientific insights, writing analysis, or drawing conclusions.","quote_label":"Author use of AI","scores":{"D1":2,"D2":2,"D3":2,"D4":2,"D5":2,"D6":2},"segment":"publisher","twilight":true,"url":"https://academic.oup.com/pages/for-authors/books/author-use-of-artificial-intelligence"},{"c2_fit":"fits","c3":"Evidential","ca":12,"coded_date":"2026-06-22","id":"sage","name":"SAGE Publishing","posture":"Balanced","provenance":{"url":"https://www.sagepub.com/journals/publication-ethics-policies/artificial-intelligence-policy","verify_status":"ok"},"quote":"We distinguish various uses for AI: assistive (no longer requiring disclosure), generative (requiring disclosure), and prohibitive.","quote_label":"AI policy","scores":{"D1":2,"D2":2,"D3":2,"D4":2,"D5":2,"D6":2},"segment":"publisher","twilight":true,"url":"https://www.sagepub.com/journals/publication-ethics-policies/artificial-intelligence-policy"},{"c2_fit":"fits","c3":"Both-split","ca":11,"coded_date":"2026-06-22","id":"ieee","name":"IEEE","posture":"Balanced","provenance":{"url":"https://open.ieee.org/author-guidelines-for-artificial-intelligence-ai-generated-text/","verify_status":"ok"},"quote":"The use of content generated by artificial intelligence in an article shall be disclosed in the acknowledgments section.","quote_label":"Author guidelines for AI-generated text","scores":{"D1":2,"D2":2,"D3":2,"D4":2,"D5":1,"D6":2},"segment":"computing-society","twilight":false,"url":"https://open.ieee.org/author-guidelines-for-artificial-intelligence-ai-generated-text/"},{"c2_fit":"fits","c3":"Evidential","ca":12,"coded_date":"2026-06-22","id":"pnas","name":"PNAS","posture":"Balanced","provenance":{"url":"https://www.pnas.org/author-center/editorial-and-journal-policies","verify_status":"ok"},"quote":"The software cannot be listed as an author because it does not meet the criteria for authorship and cannot share responsibility for the paper or be held accountable for the integrity of the data reported.","quote_label":"Editorial and journal policies","scores":{"D1":2,"D2":2,"D3":2,"D4":2,"D5":2,"D6":2},"segment":"publisher","twilight":true,"url":"https://www.pnas.org/author-center/editorial-and-journal-policies"},{"c2_fit":"fits","c3":"Both-split","ca":10,"coded_date":"2026-06-22","id":"jama","name":"JAMA Network","posture":"Balanced","provenance":{"url":"https://jamanetwork.com/journals/jama/fullarticle/2807956","verify_status":"ok"},"quote":"Attribution of authorship carries with it accountability for the work, and AI tools cannot take such responsibility.","quote_label":"Instructions for authors","scores":{"D1":2,"D2":2,"D3":2,"D4":1,"D5":1,"D6":2},"segment":"med-journal","twilight":true,"url":"https://jamanetwork.com/journals/jama/fullarticle/2807956"},{"c2_fit":"fits","c3":"Both-split","ca":9,"coded_date":"2026-06-22","id":"nejm","name":"New England Journal of Medicine","posture":"Balanced","provenance":{"url":"https://ai.nejm.org/about/editorial-policies","verify_status":"ok"},"quote":"Because the authors of a manuscript are responsible for the accuracy, integrity, and originality of the work, chatbots or other AI-assisted technologies cannot be listed as authors.","quote_label":"NEJM AI editorial policies","scores":{"D1":1,"D2":2,"D3":2,"D4":1,"D5":2,"D6":1},"segment":"med-journal","twilight":false,"url":"https://ai.nejm.org/about/editorial-policies"},{"c2_fit":"fits","c3":"Both-split","ca":12,"coded_date":"2026-06-22","id":"wame","name":"World Association of Medical Editors","posture":"Balanced","provenance":{"url":"https://wame.org/page3.php?id=106","verify_status":"ok"},"quote":"In the interests of enabling scientific scrutiny, including replication and identifying falsification, the full prompt used to generate the research results, the time and date of query, and the AI tool used and its version, should be provided.","quote_label":"Recommendations on chatbots & generative AI","scores":{"D1":2,"D2":2,"D3":2,"D4":2,"D5":2,"D6":2},"segment":"med-integrity","twilight":true,"url":"https://wame.org/page3.php?id=106"},{"c2_fit":"fits","c3":"Both-split","ca":10,"coded_date":"2026-06-22","id":"cse","name":"Council of Science Editors","posture":"Balanced","provenance":{"url":"https://www.csescienceeditor.org/article/cse-guidance-on-machine-learning-and-artificial-intelligence-tools/","verify_status":"ok"},"quote":"A nonhuman cannot be responsible or accountable for the accuracy, integrity, and originality of the work.","quote_label":"Guidance on machine learning and AI tools","scores":{"D1":2,"D2":2,"D3":2,"D4":1,"D5":1,"D6":2},"segment":"science-editors","twilight":true,"url":"https://www.csescienceeditor.org/article/cse-guidance-on-machine-learning-and-artificial-intelligence-tools/"},{"c2_fit":"fits","c3":"Both-split","ca":10,"coded_date":"2026-06-22","id":"royal-society","name":"The Royal Society","posture":"Balanced","provenance":{"url":"https://royalsociety.org/journals/ethics-policies/openness/","verify_status":"ok"},"quote":"Such systems must not replace key researcher tasks such as producing scientific insights, analysing and interpreting data.","quote_label":"Authorship, competing interests and AI","scores":{"D1":1,"D2":2,"D3":2,"D4":2,"D5":2,"D6":1},"segment":"society-publisher","twilight":true,"url":"https://royalsociety.org/journals/ethics-policies/openness/"},{"c2_fit":"fits","c3":"Both-split","ca":12,"coded_date":"2026-06-22","id":"bbc","name":"BBC","posture":"Balanced","provenance":{"url":"https://www.bbc.co.uk/editorialguidelines/guidance/use-of-artificial-intelligence","verify_status":"ok"},"quote":"BBC use of AI must never undermine the trust of audiences.","quote_label":"Editorial guidance on AI (2025-06-23)","scores":{"D1":2,"D2":2,"D3":2,"D4":2,"D5":2,"D6":2},"segment":"journalism","twilight":true,"url":"https://www.bbc.co.uk/editorialguidelines/guidance/use-of-artificial-intelligence"},{"c2_fit":"fits","c3":"Evidential","ca":11,"coded_date":"2026-06-22","id":"reuters-news","name":"Reuters (news agency)","posture":"Balanced","provenance":{"url":"https://www.thomsonreuters.com/en/about-us/trust-principles","verify_status":"ok"},"quote":"Our images and stories must reflect reality.","quote_label":"Handbook of Journalism","scores":{"D1":2,"D2":2,"D3":1,"D4":2,"D5":2,"D6":2},"segment":"journalism","twilight":false,"url":"https://www.thomsonreuters.com/en/about-us/trust-principles"},{"c2_fit":"fits","c3":"Both-split","ca":11,"coded_date":"2026-06-22","id":"guardian","name":"The Guardian","posture":"Balanced","provenance":{"url":"https://uploads.guim.co.uk/2026/03/03/Editorial_Code_of_Practice_Guidelines_March2026.pdf","verify_status":"ok"},"quote":"Guardian audiences are entitled to expect that work that appears under your byline has been authored by you.","quote_label":"Editorial Code §H (2026-03)","scores":{"D1":2,"D2":2,"D3":2,"D4":1,"D5":2,"D6":2},"segment":"journalism","twilight":true,"url":"https://uploads.guim.co.uk/2026/03/03/Editorial_Code_of_Practice_Guidelines_March2026.pdf"},{"c2_fit":"fits","c3":"Both-split","ca":12,"coded_date":"2026-06-22","id":"nyt","name":"The New York Times","posture":"Prohibitive","provenance":{"url":"https://www.nytco.com/press/principles-for-using-generative-a.i.-in-the-timess-newsroom/","verify_status":"secondary-blocked"},"quote":"We don\'t use A.I. to write articles, and journalists are ultimately responsible for everything that we publish.","quote_label":"Newsroom principles (secondary-sourced)","scores":{"D1":2,"D2":2,"D3":2,"D4":2,"D5":2,"D6":2},"segment":"journalism","twilight":true,"url":"https://www.nytco.com/press/principles-for-using-generative-a.i.-in-the-timess-newsroom/"},{"c2_fit":"fits","c3":"Evidential","ca":9,"coded_date":"2026-06-22","id":"spj","name":"Society of Professional Journalists","posture":"Balanced","provenance":{"url":"https://www.spj.org/spj-code-of-ethics/","verify_status":"ok"},"quote":"Take responsibility for the accuracy of their work. Verify information before releasing it. Use original sources whenever possible.","quote_label":"Code of Ethics","scores":{"D1":2,"D2":1,"D3":2,"D4":1,"D5":1,"D6":2},"segment":"journalism","twilight":false,"url":"https://www.spj.org/spj-code-of-ethics/"},{"c2_fit":"partially","c3":"Both-split","ca":5,"coded_date":"2026-06-22","id":"arl","name":"Association of Research Libraries","posture":"Enabling","provenance":{"url":"https://www.arl.org/resources/research-libraries-guiding-principles-for-artificial-intelligence/","verify_status":"ok"},"quote":"Libraries believe \'no human, no AI.\'","quote_label":"Guiding Principles for AI","scores":{"D1":1,"D2":1,"D3":0,"D4":1,"D5":1,"D6":1},"segment":"library","twilight":true,"url":"https://www.arl.org/resources/research-libraries-guiding-principles-for-artificial-intelligence/"},{"c2_fit":"contradicts","c3":"Relational","ca":3,"coded_date":"2026-06-22","id":"educause","name":"EDUCAUSE","posture":"Balanced","provenance":{"url":"https://er.educause.edu/articles/2023/12/cross-campus-approaches-to-building-a-generative-ai-policy","verify_status":"ok"},"quote":"[The policy creates] an untenable situation for students who must somehow defend themselves against a machine that cannot show its work but is just a projection.","quote_label":"Cross-Campus Approaches to a GenAI Policy","scores":{"D1":0,"D2":1,"D3":1,"D4":0,"D5":0,"D6":1},"segment":"edtech","twilight":true,"url":"https://er.educause.edu/articles/2023/12/cross-campus-approaches-to-building-a-generative-ai-policy"},{"c2_fit":"partially","c3":"Relational","ca":9,"coded_date":"2026-06-22","id":"unesco","name":"UNESCO — GenAI in education & research","posture":"Prohibitive","provenance":{"url":"https://www.unesco.org/en/articles/guidance-generative-ai-education-and-research","verify_status":"ok"},"quote":"A human-centred approach requires proper regulation that can ensure human agency, transparency and public accountability.","quote_label":"Guidance for generative AI in education and research","scores":{"D1":1,"D2":2,"D3":1,"D4":2,"D5":2,"D6":1},"segment":"intergov","twilight":true,"url":"https://www.unesco.org/en/articles/guidance-generative-ai-education-and-research"},{"c2_fit":"fits","c3":"Evidential","ca":10,"coded_date":"2026-06-22","id":"oecd","name":"OECD AI Principles","posture":"Enabling","provenance":{"url":"https://oecd.ai/en/ai-principles","verify_status":"ok"},"quote":"AI actors should ensure traceability, including in relation to datasets, processes and decisions made during the AI system lifecycle, to enable analysis of the AI system\'s outputs and responses to inquiry.","quote_label":"AI Principles (OECD/LEGAL/0449)","scores":{"D1":2,"D2":2,"D3":2,"D4":1,"D5":1,"D6":2},"segment":"intergov","twilight":false,"url":"https://oecd.ai/en/ai-principles"},{"c2_fit":"partially","c3":"Both-split","ca":8,"coded_date":"2026-06-22","id":"us-doe-oet","name":"US Dept of Education (OET)","posture":"Balanced","provenance":{"url":"https://www.ed.gov/sites/ed/files/documents/ai-report/ai-report.pdf","verify_status":"ok"},"quote":"A top priority with AI is to keep humans in the loop and in control.","quote_label":"AI and the Future of Teaching and Learning","scores":{"D1":1,"D2":2,"D3":1,"D4":1,"D5":2,"D6":1},"segment":"gov-education","twilight":true,"url":"https://www.ed.gov/sites/ed/files/documents/ai-report/ai-report.pdf"}]'
CORPUS = json.loads(_CORPUS_JSON)


# ----------------------------------------------------------- helpers ----

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
    }


def _find(corpus, needle):
    """Match by exact id, then case-insensitive name/id substring."""
    if not needle:
        return None
    n = str(needle).strip().lower()
    for c in corpus:
        if str(c.get("id", "")).lower() == n:
            return c
    for c in corpus:
        if n in str(c.get("name", "")).lower() or n in str(c.get("id", "")).lower():
            return c
    return None


# ----------------------------------------------------------- handlers ----

def handle_lookup(corpus, args):
    c = _find(corpus, args.get("institution"))
    if not c:
        return {"error": "no institution matching %r" % args.get("institution"),
                "hint": "try ca_index_search to list ids/names"}
    return _full(c)


def handle_search(corpus, args):
    posture = (args.get("posture") or "").strip().lower() or None
    logic = (args.get("trust_logic") or "").strip().lower() or None
    segment = (args.get("segment") or "").strip().lower() or None
    fit = (args.get("c2_fit") or "").strip().lower() or None
    min_ca = args.get("min_ca")
    max_ca = args.get("max_ca")
    twilight = args.get("twilight")
    out = []
    for c in corpus:
        if posture and str(c.get("posture", "")).lower() != posture:
            continue
        if logic and str(c.get("c3", "")).lower() != logic:
            continue
        if segment and segment not in str(c.get("segment", "")).lower():
            continue
        if fit and str(c.get("c2_fit", "")).lower() != fit:
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
    a = _find(corpus, args.get("a"))
    b = _find(corpus, args.get("b"))
    missing = [k for k, v in (("a", a), ("b", b)) if v is None]
    if missing:
        return {"error": "could not resolve: %s" % ", ".join(
            "%s=%r" % (m, args.get(m)) for m in missing)}
    fa, fb = _full(a), _full(b)
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
        "corpus_snapshot": CORPUS_SNAPSHOT,
    }


def handle_methodology(corpus, args):
    return {
        "instrument": {
            "scale": "0-12 composite (six dimensions, 0-2 each)",
            "dimensions": [{"key": d, "label": DIM_LABELS[d]} for d in DIMENSIONS],
            "fields": {
                "ca": "Composite Calibrated Authority score, sum of D1-D6 (0-12).",
                "posture": "Prohibitive | Balanced | Enabling.",
                "c2_fit": "Verification-boundary fit (fits | partial | contradicts).",
                "c3": "Trust-logic: Evidential | Relational | Both-split | Neither.",
                "twilight": "Uses precedent-collapse / feedback-delay / exponential-fog framing.",
            },
        },
        "how_to_cite": "Reitz, C.H. The Calibrated Authority Index. " + _BASE_URL,
        "license": "CC-BY-4.0",
        "methodology_url": _BASE_URL + "/methodology",
        "manifest_url": _BASE_URL + "/institutions/index.json",
        "engine_version": ENGINE_VERSION,
        "corpus_snapshot": CORPUS_SNAPSHOT,
    }


TOOLS = [
    {
        "name": "ca_index_lookup",
        "description": "Look up one institution's Calibrated Authority record by name or id "
                       "(e.g. 'Nature', 'educause'). Returns the six scores, composite CA, "
                       "trust-logic, the verbatim policy quote, source URL, and permalink.",
        "inputSchema": {
            "type": "object",
            "properties": {"institution": {"type": "string",
                           "description": "Institution name or id."}},
            "required": ["institution"],
        },
        "handler": handle_lookup,
    },
    {
        "name": "ca_index_search",
        "description": "Filter the index. Any combination of posture (Prohibitive|Balanced|Enabling), "
                       "trust_logic (Evidential|Relational|Both-split|Neither), c2_fit "
                       "(fits|partial|contradicts), segment substring, min_ca/max_ca (0-12), "
                       "twilight (bool). Returns matching institutions sorted by CA.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "posture": {"type": "string"},
                "trust_logic": {"type": "string"},
                "c2_fit": {"type": "string"},
                "segment": {"type": "string"},
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
                       "which of the six dimensions differ.",
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


def dispatch_tool(name, args, corpus=None):
    """Run a tool by name. Returns (result, is_error)."""
    if name not in _HANDLERS:
        return {"error": "unknown tool %r" % name}, True
    if corpus is None:
        corpus = CORPUS
    try:
        result = _HANDLERS[name](corpus, args or {})
        is_error = isinstance(result, dict) and "error" in result
        return result, is_error
    except Exception as e:  # defensive
        return {"error": "%s: %s" % (type(e).__name__, e)}, True


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
        })

    def do_DELETE(self):
        # Stateless server: no sessions to terminate.
        self._send_json(405, {"error": "method not allowed (stateless server, no sessions)"})
