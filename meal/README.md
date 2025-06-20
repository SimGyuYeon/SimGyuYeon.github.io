# [meal](https://SimGyuYeon.github.io/meal/index)

# 🍽️ 우리집 저녁 메뉴 기록 관리

가족과 함께 저녁 식단을 계획하고, 냉장고 재료 및 식비를 관리하는 웹 애플리케이션입니다.  
GitHub Pages + Notion API + Cloudflare Workers 기반으로 동작하며, 데이터는 Notion 데이터베이스에 저장됩니다.

---

## ✅ 주요 기능

- **식단 계획 등록 및 조회**
- **냉장고 재료 관리 (수량, 단위 포함)**
- **과거 식사 기록 관리**
- **수정 및 삭제 기능**
- **월별 식비 집계 (향후 추가 가능)**
- **모바일 대응 디자인 (반응형, Apple 스타일 UI)**

---

## 🛠️ 기술 스택

| 항목 | 기술 |
|------|------|
| 프론트엔드 | HTML, CSS, JavaScript, Axios |
| 백엔드 (중계) | Cloudflare Workers |
| 데이터베이스 | Notion API (3개의 테이블: meals, fridge, plans) |
| 배포 | GitHub Pages |

---

## 🗂️ 디렉토리 구조
```bash
/ (루트 디렉토리)
├── index.html       # 메인 HTML 페이지
├── style.css        # Apple 스타일 반응형 CSS
├── main.js          # Axios 기반 동작 스크립트 (CRUD)
└── README.md        # 프로젝트 설명서
```

---

## 🔌 연동된 Notion 테이블

1. **meals**: 과거 식사 기록 (이름, 날짜, 배달/외식 여부, 가격 등)
2. **fridge**: 냉장고 재료 목록 (이름, 수량, 단위, 유통기한)
3. **plans**: 향후 식단 계획 (이름, 날짜, 재료, 가격)

> ⚙️ Cloudflare Worker를 통해 CORS 문제 없이 Notion API에 안전하게 접근합니다.

---

## 📦 사용 방법

1. 이 저장소를 클론하거나 `index.html`, `style.css`, `main.js` 파일을 GitHub Pages에서 호스팅합니다.
2. Cloudflare Workers 백엔드를 설정합니다 (환경변수에 Notion API 키 및 DB ID 포함).
3. Notion에 템플릿 데이터베이스를 설정하고 공유 링크로 연동합니다.
4. 페이지 접속 후 식단, 재료, 기록 정보를 입력하고 저장합니다.

---

## 🚧 앞으로 할 일

- [ ] 월별 식비 자동 집계
- [ ] 재료 유통기한 경고 기능
- [ ] 주간 식단 추천 기능 (냉장고 재료 기반)
- [ ] 로그인 없이 다른 가족 구성원과 협업 가능하게 하기

---

## 👨‍👩‍👧 사용 목적

- 부부가 함께 식단과 식비를 투명하게 관리
- 냉장고 재고 확인 후 불필요한 식재료 구매 방지
- 배달 및 외식 횟수 줄이기 위한 동기 부여

---

## 🔐 개인정보 및 보안

- Notion API 키는 절대 GitHub에 공개되지 않도록 `.env` 설정은 Cloudflare Worker 환경변수에서 관리합니다.
- 백엔드와 프론트는 완전히 분리되어 있어 GitHub Pages에 데이터가 저장되지 않습니다.

