# Git 브랜치 병합 작업 정리

- 작업 브랜치: `ayeon`, `236`
- 중간 병합 브랜치: `test`
- 최종 병합 브랜치: `main`

---

## ✅ 전체 Git 명령어 스크립트



# Git 명령어 정리 스크립트

# 1. 특정 브랜치만 클론하기 
git clone -b develop --single-branch https://github.com/user/project.git
cd project  # 클론된 디렉토리로 이동

# 2. 특정 브랜치로 이동 (예: test 브랜치 작업 시작 전)
git checkout test
git pull origin test  # 원격 test 브랜치 최신 내용 반영

# 3. 작업 브랜치 병합 (ayeon 브랜치)
git fetch origin
git merge origin/ayeon

# 충돌이 생길 경우 수동으로 해결하고 아래 명령 실행
git add .
git commit -m "Merge ayeon into test"

# 4. 다음 작업 브랜치 병합 (236 브랜치)
git merge origin/236

# 충돌 시 동일하게 처리
git add .
git commit -m "Merge 236 into test"

# 5. test 브랜치 원격 저장소에 푸시
git push origin test

# 6. main 브랜치로 이동 및 병합
git checkout main
git pull origin main
git merge test

# 7. 최종적으로 main 브랜치에 푸시
git push origin main
