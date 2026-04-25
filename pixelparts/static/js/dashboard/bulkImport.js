document.addEventListener("DOMContentLoaded",function(){
    const fileInput = document.querySelector("#importFile"); //hidden <input type="file" id="importFile">
    const importLink = document.querySelector("#bulkImport"); //the import products link


    //clicking the link triggers the hidden file picker
    importLink.addEventListener("click",function(e){
        e.preventDefault();
        fileInput.click();
    })

    //fire when the user selects a file
    fileInput.addEventListener("change",async function(){
        const file = fileInput.files[0];
        if (!file) return;

        const data = new FormData();
        data.append("file",file);
        // CSRF token from the delete modal form thats on the same page (products.html)
        data.append("csrfmiddlewaretoken",document.querySelector('[name=csrfmiddlewaretoken]').value);

        try{
            //send the file to the server, alert the user with the result
            const response = await fetch("/dashboard/bulk_import/",{
                method:"POST",
                body:data
            })
            const json = await response.json();
            if (json.error){
                alert("Something went wrong: "+json.error)
            }
            else{
                alert("File Uploaded Successfully");
            }

        } catch(e){
            alert("Something went wrong: "+e);
        }
    })
})