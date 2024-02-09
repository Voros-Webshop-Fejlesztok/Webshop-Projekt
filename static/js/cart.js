var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product
        var action = this.dataset.action
        
        console.log(user)
        if(user == 'AnonymousUser'){
            console.log('Not logged in')
        }else{
            updateUserOrder(productId, action)
        }
    })   
}

function updateUserOrder(productId, action){

    var url = '/update_item/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken
        },
        body:JSON.stringify({'productId': productId, 'action':action})
    })
    .then((response) => {
        return response.json()
    })

    .then((data) => {
        var path = window.location.pathname;
        if (path == "/store/") {
            succesfulOrder()
        }else{
            location.reload()
        }

    })
}

function succesfulOrder() {
    document.getElementById("popup").style.display = 'block';
    document.getElementById('formContent').style.opacity = '0.1';
    var popupClose = document.getElementById("popupClose");
    popupClose.addEventListener("click", function () {
        document.getElementById("popup").style.display = 'none';
        document.getElementById('formContent').style.opacity = '1';
    });
}

    