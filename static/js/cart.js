var updateBtns = document.getElementsByClassName("update-cart");

for (i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener("click", function () {
    var productId = this.dataset.product;
    var action = this.dataset.action;

    if (user == "AnonymousUser") {
      addCookieItem(productId, action);
      var path = window.location.pathname;
        if (path == "/store/") {
            succesfulOrder()
        }else{
            location.reload()
        }
    } else {
      updateUserOrder(productId, action);
    }
  });
}

function addCookieItem(productId, action) {
  console.log("User is not authenticated");

  if (action == "add") {
    if (cart[productId] == undefined) {
      cart[productId] = { quantity: 1 };
    } else {
      cart[productId]["quantity"] += 1;
    }
  }

  if (action == "remove") {
    cart[productId]["quantity"] -= 1;

    if (cart[productId]["quantity"] <= 0) {
      console.log("Item should be deleted");
      delete cart[productId];
    }
  }

  console.log('Cart:', cart);
  document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/";
  location.reload
}

function updateUserOrder(productId, action) {
  var url = "/update_item/";

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ productId: productId, action: action }),
  })
    .then((response) => {
      return response.json();
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
      document.getElementById("popup").style.animation = "checkoutClose 0.5s ease-in-out"

      setTimeout(function() {
        document.getElementById("popup").style.display = 'none';
        document.getElementById('formContent').style.opacity = '1';
        document.getElementById("popup").style.animation = "";
        location.reload()
    }, 500);
  
  });
    
    setTimeout(closePopup, 2000);

    function closePopup() {
      document.getElementById("popup").style.animation = "checkoutClose 0.5s ease-in-out"

      setTimeout(function() {
        document.getElementById("popup").style.display = 'none';
        document.getElementById('formContent').style.opacity = '1';
        document.getElementById("popup").style.animation = "";
        location.reload()
    }, 500);
    }
    
}