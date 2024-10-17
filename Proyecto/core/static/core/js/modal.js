const table = document.getElementById ('myTable')
const modal = document.getElementById ('modal')
const inputs = document.querySelectorAll ('input')

let count=0;



table.addEventListener('click',(e)=>{
    e.stopPropagation();
    let data = e.target.parentElement.parentElement.children;

    fillData(data)
    modal.classList.toggle('modal fade')
})

const fillData = (data) =>{
    for(let index of inputs){
        count+=1
        index.value = data[count].textContent
        console.log(index)

    }
}