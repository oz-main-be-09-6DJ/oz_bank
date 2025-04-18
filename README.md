![Copy of 6dj_bank](https://github.com/user-attachments/assets/a4ed9409-4bd0-456e-9dba-1bb3d844bd63)

# 📌 Database Schema

* 이 프로젝트의 데이터베이스 스키마에 대한 설명입니다.
* 각 테이블의 역할과 테이블 간의 관계는 다음과 같습니다.

---

## 📂 테이블 설명

### **1. User 테이블 (`user`)
- 사용자의 기본 정보를 저장하는 테이블입니다.
- **Primary Key**: `id` (UUID)
- **Columns**:
  - `email` (VARCHAR(255), UNIQUE, NOT NULL) : 사용자 이메일
  - `name` (VARCHAR(50), NOT NULL) : 사용자 이름
  - `nick_name` (VARCHAR(50), NULL) : 사용자 닉네임
  - `phone_number` (VARCHAR(20), UNIQUE, NULL) : 휴대폰 번호
  - `password` (TEXT, NOT NULL) : 비밀번호
  - `type` (VARCHAR(10), NOT NULL) : 사용자 유형 (예: admin, user)
  - `authentication` (BOOLEAN) : 인증 여부
  - `notification` (BOOLEAN) : 알림 설정 여부
  - `create_at`, `deleted_at`, `updated_at` : 생성, 삭제, 수정 일자

---

### **2. Account 테이블 (`account`)
- 사용자의 계좌 정보를 저장하는 테이블입니다.
- **Primary Key**: `id` (UUID)
- **Columns**:
  - `account_number` (VARCHAR(20), UNIQUE, NOT NULL) : 계좌 번호
  - `bank_code` (VARCHAR(10), NOT NULL) : 은행 코드
  - `account_type` (VARCHAR(20), NOT NULL) : 계좌 유형
  - `balance` (DECIMAL(14,2), NOT NULL) : 계좌 잔액
  - `created_at`, `deleted_at`, `updated_at` : 생성, 삭제, 수정 일자
  - `user_id` (UUID) : **User 테이블의 Foreign Key** (1:N 관계)

---

### **3. Transaction History 테이블 (`transaction_history`)
- 사용자의 거래 내역을 저장하는 테이블입니다.
- **Primary Key**: `id` (UUID)
- **Columns**:
  - `trader_id` (INT, NOT NULL) : 거래 상대방 ID
  - `transaction_amount` (INT, NOT NULL) : 거래 금액
  - `transaction_balance` (INT, NOT NULL) : 거래 후 잔액
  - `transaction_details` (VARCHAR(255)) : 거래 상세 내용
  - `type` (VARCHAR(10), ENUM) : 거래 유형 (예: 입금, 출금)
  - `method` (VARCHAR(20), ENUM) : 거래 방법 (예: 카드, 계좌이체)
  - `created_at` (TIMESTAMP DEFAULT NOW()) : 거래 생성 날짜
  - `id2` (UUID) : **Account 테이블의 Foreign Key** (1:N 관계)

---

### **4. Notification 테이블 (`notification`)
- 사용자의 알림 정보를 저장하는 테이블입니다.
- **Primary Key**: `id` (UUID)
- **Columns**:
  - `message` (VARCHAR(100), NOT NULL) : 알림 메시지
  - `is_read` (BOOLEAN DEFAULT FALSE, NOT NULL) : 읽음 여부
  - `created_at` (TIMESTAMPTZ, NOT NULL) : 알림 생성 일자
  - `user_id` (UUID) : **User 테이블의 Foreign Key** (1:N 관계)

---

### **5. Analysis 테이블 (`analysis`)
- 사용자의 분석 데이터를 저장하는 테이블입니다.
- **Primary Key**: `id` (UUID)
- **Columns**:
  - `analysis_about` (VARCHAR(20), ENUM, NOT NULL) : 분석 대상
  - `analysis_type` (VARCHAR(10), ENUM, NOT NULL) : 분석 유형
  - `period_start` (DATETIME, NOT NULL) : 분석 시작 기간
  - `period_end` (DATETIME, NOT NULL) : 분석 종료 기간
  - `analysis_description` (VARCHAR(100), NOT NULL) : 분석 설명
  - `result_image` (TEXT, NULL) : 분석 결과 이미지
  - `created_at`, `updated_at` : 생성, 수정 일자
  - `user_id` (UUID) : **User 테이블의 Foreign Key** (1:N 관계)

---

## 🔗 테이블 간의 관계

1. **User (1) : (N) Account**  
   - 한 명의 사용자는 여러 개의 계좌(Account)를 가질 수 있음.  
   - `user_id`가 `account` 테이블의 Foreign Key.  

2. **User (1) : (N) Notification**  
   - 한 명의 사용자는 여러 개의 알림(Notification)을 받을 수 있음.  
   - `user_id`가 `notification` 테이블의 Foreign Key.  

3. **User (1) : (N) Analysis**  
   - 한 명의 사용자는 여러 개의 분석 데이터(Analysis)를 가질 수 있음.  
   - `user_id`가 `analysis` 테이블의 Foreign Key.  

4. **Account (1) : (N) Transaction History**  
   - 하나의 계좌(Account)에는 여러 개의 거래 내역(Transaction History)이 존재할 수 있음.  
   - `id2`가 `transaction_history` 테이블의 Foreign Key.  

## ✅ Model을 바탕으로 테스트코드 실행 결과
![스크린샷 2025-04-03 오후 8 31 13](https://github.com/user-attachments/assets/24e261b1-d1e9-4fd3-9925-eb0e04435ac8)

## ✅ Flow Chart
### * 회원가입 Flow Chart
![oz_bank-1_회원가입_순서도 drawio](https://github.com/user-attachments/assets/82105d3f-c745-4332-85c0-7d0b2f27dd22)

### * 로그인/로그아웃 Flow Chart
![oz_bank-2_로그인_로그아웃_순서도 drawio](https://github.com/user-attachments/assets/82d59fec-3c5f-4dcb-838c-12565bc0d488)

## ✅ 소셜 로그인 (네이버)
<img width="911" alt="스크린샷 2025-04-04 오전 6 40 46" src="https://github.com/user-attachments/assets/9e8a934a-508c-4e90-b47a-652bbba93ac5" />

1.로그인버튼 클릭 : 사용자가 A 앱에서 네이버 로그인하기 버튼을 누른다.
    - A 앱 클라이언트에서 네이버 OAuth 인증 페이지로 리다이렉트 요청을 보냄

2.로그인요청 : 네이버의 인증서버로 리다이렉트 됨 : 네이버 로그인 창에서 인증을 진행

3.인가코드 전송 : 인증 성공하면 인가코드가 발급 됨 (네이버가 보장함)

4.인가코드 전송 : A 앱 클라이언트가 인가 코드를 받아서 A 앱 서버로 전달
    - 클라이언트가 인가 코드를 포함해서 A 앱 서버에 요청을 보냄

5.인가코드로 토큰 요청 : A 앱 서버에서 이 인가코드를 사용해서 네이버 인증 서버에 액세스 토큰을 요청함

6.토큰전달 : 네이버 인증서버가 요청을 검증하고 액세스 토큰 & 리프레시 토큰을 반환 (네이버 서버 -> A 앱 서버)

7.클라이언트가 이 액세스 토큰을 사용해서 A의 리소스 서버에 접근할 수 있음
