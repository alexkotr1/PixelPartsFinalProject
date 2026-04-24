document.addEventListener("DOMContentLoaded",function(){
    const fileInput = document.querySelector("#importFile");
    const importLink = document.querySelector("#bulkImport");


    importLink.addEventListener("click",function(e){
        e.preventDefault();
        fileInput.click();
    })

    fileInput.addEventListener("change",async function(){
        const file = fileInput.files[0];
        if (!file) return;

        const data = new FormData();
        data.append("file",file);
        data.append("csrfmiddlewaretoken",document.querySelector('[name=csrfmiddlewaretoken]').value);

        try{
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
            console.log(typeof e);
            console.log(e);
            alert("Something went wrong2: "+e);
        }
    })
})