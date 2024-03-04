const submitBtn = document.querySelector("#add_cupcake_btn");
const ipFlavor = document.querySelector("#ip_flavor");
const ipSize = document.querySelector("#ip_size");
const ipRating = document.querySelector("#ip_rating");
const ipImage = document.querySelector("#ip_image");
const $displayList = $("#display_ul");
BASE_URL = "http://127.0.0.1:5000";

async function start(){
    await getCupcakes();
}

submitBtn.addEventListener("click", async function(e){
    e.preventDefault();
    d = {
        "flavor": ipFlavor.value,
        "size": ipSize.value,
        "rating": ipRating.value,
        "image": ipImage.value
    }
    await addCupcake(d);
    await getCupcakes();
})

async function getCupcakes(){
    const res = await axios({
        url:`${BASE_URL}/api/cupcakes`,
        method:"GET"
    });
    $displayList.empty();
    for (i=0; i < res.data.cupcakes.length; i++){
        const $cupcake = `<li>${res.data.cupcakes[i].flavor}</li>`;
        $displayList.append($cupcake);
    }
}

async function addCupcake(data){
    try{
        const res = await axios({
            url: `${BASE_URL}/api/cupcakes`,
            method: "POST",
            data: data
        })
        alert("New cupcake added!!!");
    } catch (error){
        console.error("Error adding cupcake:", error);
        alert("Error adding cupcake!")
    }
}
start();