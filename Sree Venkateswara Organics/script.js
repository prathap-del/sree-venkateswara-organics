let cart = JSON.parse(localStorage.getItem("cart")) || [];


/* ADD PRODUCT TO CART */

function addToCart(name, price) {

    const existingProduct = cart.find(
        product => product.name === name
    );

    if (existingProduct) {

        existingProduct.quantity =
            existingProduct.quantity + 1;

    } else {

        cart.push({
            name: name,
            price: price,
            quantity: 1
        });

    }

    saveCart();

    updateCart();

    alert(name + " added to cart!");
}


/* SAVE CART */

function saveCart() {

    localStorage.setItem(
        "cart",
        JSON.stringify(cart)
    );

}


/* UPDATE CART */

function updateCart() {

    const cartCount =
        document.getElementById("cartCount");

    let totalQuantity = 0;

    cart.forEach(function(product) {

        totalQuantity =
            totalQuantity + product.quantity;

    });


    if (cartCount) {

        cartCount.innerText = totalQuantity;

    }


    const cartItems =
        document.getElementById("cartItems");

    if (!cartItems) {

        return;

    }


    cartItems.innerHTML = "";

    let total = 0;


    if (cart.length === 0) {

        cartItems.innerHTML =
            "<p>Your cart is empty.</p>";

    }


    cart.forEach(function(product, index) {

        const productTotal =
            product.price * product.quantity;

        total = total + productTotal;


        cartItems.innerHTML += `

            <div class="cart-item">

                <div>

                    <strong>
                        ${product.name}
                    </strong>

                    <br>

                    ₹${product.price} ×
                    ${product.quantity}

                    <br>

                    Total: ₹${productTotal}

                </div>

                <button
                    class="remove-button"
                    onclick="removeFromCart(${index})">
                    Remove
                </button>

            </div>

        `;

    });


    const cartTotal =
        document.getElementById("cartTotal");


    if (cartTotal) {

        cartTotal.innerText = total;

    }

}


/* REMOVE PRODUCT */

function removeFromCart(index) {

    cart.splice(index, 1);

    saveCart();

    updateCart();

}


/* OPEN CART */

function openCart() {

    updateCart();

    const cartModal =
        document.getElementById("cartModal");

    if (cartModal) {

        cartModal.style.display = "flex";

    }

}


/* CLOSE CART */

function closeCart() {

    const cartModal =
        document.getElementById("cartModal");

    if (cartModal) {

        cartModal.style.display = "none";

    }

}


/* FILTER PRODUCTS */

function filterProducts(category) {

    const products =
        document.querySelectorAll(".product-card");


    products.forEach(function(product) {

        if (category === "all") {

            product.style.display = "block";

        }

        else if (
            product.classList.contains(category)
        ) {

            product.style.display = "block";

        }

        else {

            product.style.display = "none";

        }

    });

}


/* CHECKOUT */

function checkout() {

    if (cart.length === 0) {

        alert("Your cart is empty.");

        return;

    }


    saveCart();

    window.location.href =
        "checkout.html";

}


/* LOAD CART WHEN PAGE OPENS */

document.addEventListener(
    "DOMContentLoaded",
    function() {

        updateCart();

    }
);