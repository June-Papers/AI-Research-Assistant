`
# 📈 AI-Research-Assistant
### RAG 기반 AI 기업 리서치 자동화 시스템

> 기업명을 입력하면 최신 뉴스와 DART 공시를 수집하고, RAG(Retrieval-Augmented Generation)를 활용하여 기업 분석 리포트를 자동 생성하는 AI 시스템입니다.

---

# 프로젝트 소개

Financial Research Assistant는 기업 리서치 업무를 자동화하기 위해 개발한 AI 기반 기업 분석 시스템입니다.

사용자가 기업명을 입력하면

- 최신 뉴스 수집
- DART 사업보고서 및 분기보고서 수집
- 문서 전처리
- RAG 기반 검색
- GPT 기반 기업 분석 리포트 생성

까지의 과정을 자동으로 수행합니다.

본 프로젝트는 금융 데이터 분석과 생성형 AI를 결합하여 실제 애널리스트의 리서치 프로세스를 자동화하는 것을 목표로 합니다.

---

# 주요 기능

- 최신 뉴스 자동 수집
- DART 사업보고서 다운로드
- DART 분기보고서 다운로드
- XML 문서 파싱
- 의미 기반 Chunk 생성
- OpenAI Embedding 생성
- FAISS 기반 Vector Search
- GPT 기반 기업 분석 리포트 생성
- Markdown/PDF 리포트 출력

---

# 시스템 아키텍처

```
                     기업명 입력
                           │
                           ▼
                    데이터 수집 계층
         ┌─────────────┬──────────────┐
         │             │              │
      뉴스 수집     DART 공시 수집   (향후) IR자료
         │             │
         └─────────────┴──────────────┐
                                      ▼
                                문서 전처리
                                      │
                                      ▼
                                  Chunk 생성
                                      │
                                      ▼
                                 Embedding 생성
                                      │
                                      ▼
                                FAISS Vector DB
                                      │
                                      ▼
                                  Retrieval
                                      │
                                      ▼
                             GPT 리포트 생성
                                      │
                                      ▼
                              기업 분석 리포트
```

---

# 프로젝트 구조

```
financial-research-assistant/

├── app.py
├── config.py
├── requirements.txt
│
├── collectors/
│   ├── news_collector.py
│   ├── dart_collector.py
│   └── cache_manager.py
│
├── preprocess/
│   ├── parser.py
│   ├── cleaner.py
│   ├── chunker.py
│   └── metadata.py
│
├── embedding/
│   └── embedder.py
│
├── vectordb/
│   ├── faiss_manager.py
│   └── retriever.py
│
├── llm/
│   └── report_generator.py
│
├── database/
│   ├── metadata.db
│   ├── faiss.index
│   └── documents.pkl
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── reports/
│
└── docs/
```

---

# 프로젝트 동작 과정

## 1. 데이터 수집

사용자가 기업명을 입력하면 다음 데이터를 자동으로 수집합니다.

- 최근 뉴스
- DART 사업보고서
- DART 분기보고서

이미 수집한 데이터는 SQLite를 이용하여 중복 다운로드를 방지합니다.

---

## 2. 문서 전처리

수집한 문서를 분석 가능한 형태로 변환합니다.

- XML Parsing
- HTML 제거
- 불필요한 문자열 제거
- 메타데이터 생성

---

## 3. Chunk 생성

긴 문서를 의미 단위로 분할합니다.

문서를 단순히 글자 수로 나누는 것이 아니라

- 보고서 목차
- 문단
- 문맥

을 고려하여 Chunk를 생성합니다.

또한 Context Loss를 방지하기 위해 Chunk Overlap을 적용합니다.

---

## 4. Embedding 생성

각 Chunk를 OpenAI Embedding 모델을 이용하여 벡터로 변환합니다.

생성된 벡터는 FAISS에 저장됩니다.

---

## 5. Retrieval

사용자의 질문을 Embedding으로 변환한 후

Vector Search를 수행하여

가장 관련성이 높은 Chunk를 검색합니다.

---

## 6. 리포트 생성

검색된 문서를 기반으로 GPT가 기업 분석 리포트를 생성합니다.

생성되는 리포트는 다음과 같은 구조를 가집니다.

- 기업 개요
- 최근 이슈
- 사업 분석
- 최근 실적
- 투자포인트
- 리스크
- 종합 의견

---

# 기술 스택

| 분야 | 기술 |
|------|------|
| Language | Python |
| LLM | OpenAI GPT |
| Embedding | OpenAI Embedding |
| Vector DB | FAISS |
| Database | SQLite |
| Parsing | BeautifulSoup, lxml |
| PDF | PyMuPDF |
| Data Collection | DART API, News API |

---

# 데이터 처리 파이프라인

```
기업명 입력

↓

뉴스 수집

↓

DART 공시 수집

↓

문서 전처리

↓

Chunk 생성

↓

Embedding 생성

↓

FAISS 저장

↓

Relevant Chunk 검색

↓

GPT 리포트 생성
```

---

# 향후 개선 사항

- [ ] 증권사 리포트 자동 수집
- [ ] IR 자료 자동 수집
- [ ] 기업 비교 분석 기능
- [ ] 재무비율 자동 분석
- [ ] Agentic RAG 적용
- [ ] Streamlit Dashboard 개발
- [ ] PDF 자동 생성
- [ ] 기업 가치평가 기능 추가

---

# 프로젝트 목표

본 프로젝트는 생성형 AI를 활용하여 금융 리서치 업무를 자동화하는 것을 목표로 합니다.

단순히 LLM의 사전학습 지식에 의존하는 것이 아니라,

최신 뉴스와 DART 공시를 Retrieval-Augmented Generation(RAG) 구조로 검색하여

신뢰성과 최신성을 확보한 기업 분석 리포트를 생성하도록 설계하였습니다.

향후에는 다양한 금융 데이터와 AI Agent를 결합하여 기업 리서치 플랫폼으로 확장하는 것을 목표로 합니다.