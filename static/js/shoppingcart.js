var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        // store.html içinde button'ın data-product özelliği
        var productId = this.dataset.product
        var action = this.dataset.action

        console.log('product_id:', productId, 'Action:', action)

        if (user === 'AnonymousUser') {
            console.log("AnonymousUser aktif.")
        } else {
            console.log('Kullanıcı:', user)
            updateUserOrder(productId, action)
        }
    })
}

function updateUserOrder(productId, action) {
    console.log('Kullanıcı: ' + user + ' yetkili ve veri gönderiyor.')

    var url = '/store/update-item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'product_id': productId, 'action': action })
    })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            location.reload()
        });
}