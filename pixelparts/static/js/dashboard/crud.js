document.addEventListener('DOMContentLoaded', function () {
    // Listens for boostraps modal show event to populate the delete form
    document.querySelector('#deleteModal').addEventListener('show.bs.modal',
    function (event) {
        // event relatedTarget is the button that triggered the modal
        let button = event.relatedTarget;
        //fill in the product/category/user name in the "Are you sure?" text
        document.querySelector('#deleteItemName').textContent = button.dataset.itemName;
        //point the forms post action at the correct delete URL for this specific item
        document.querySelector('#deleteForm').action = button.dataset.deleteUrl;
    })
})