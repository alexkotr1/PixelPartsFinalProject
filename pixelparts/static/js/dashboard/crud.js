document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('#deleteModal').addEventListener('show.bs.modal',
    function (event) {
        let button = event.relatedTarget;
        document.querySelector('#deleteItemName').textContent = button.dataset.itemName;
        document.querySelector('#deleteForm').action = button.dataset.deleteUrl;
    })
})