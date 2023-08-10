
const video2 = document.getElementById('stream');
const snapshotButton = document.getElementById('snapshotButton');
const snapshotImage = document.getElementById('snapshotImage');
// 일치하는 id 속성을 가진 요소 찾고, 반환

snapshotButton.addEventListener('click', () => {
    // /snapshot 주소로 요청
    fetch('/snapshot')
    // 성공하면 .then을 이용해 리턴
        .then(response => response.blob()) 
        // 이미지 저장
        .then(blob => {
            const url = URL.createObjectURL(blob);
            snapshotImage.src = url;
            snapshotImage.style.display = "block";
            // 캡쳐한 이미지가 보여진다
        });
});