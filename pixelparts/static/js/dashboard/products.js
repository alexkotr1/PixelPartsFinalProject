document.addEventListener('DOMContentLoaded', function () {
    document.querySelector("#deleteModal").addEventListener('show.bs.modal',
    function (event) {
    let button = event.relatedTarget;
    document.querySelector("#deleteProductName").textContent = button.dataset.productName;
    document.querySelector('#deleteForm').action = button.dataset.deleteUrl;
})
})
