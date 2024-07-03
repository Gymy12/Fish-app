$(document).ready(function () {
  $("#loadMore").on("click", function () {
    var _currentProducts = $(".product-box").length;
    var _limit = $(this).attr("data-limit");
    var _total = $(this).attr("data-total");

    // Start Ajax
    $.ajax({
      url: "/load-more-data",
      data: {
        limit: _limit,
        offset: _currentProducts,
      },
      dataType: "json",
      beforeSend: function () {
        $("#loadMore").attr("disabled", true);
        $(".load-more-icon").addClass("fa-spin");
      },
      success: function (res) {
        $("#filteredProducts").append(res.data);
        $("#loadMore").attr("disabled", false);
        $(".load-more-icon").removeClass("fa-spin");

        var _totalShowing = $(".product-box").length;
        if (_totalShowing == _total) {
          $("#loadMore").remove();
        }
      },
    });
    // End
  });

  // Product Variation
  $(".choose-count").hide();

  // Show count according to selected quantity
  $(".choose-quantity").on("click", function () {
    $(".choose-count").removeClass("active");
    $(".choose-quantity").removeClass("focused");
    $(this).addClass("focused");

    var _quantity = $(this).attr("data-quantity");
    $(".choose-count").hide();
    $(".quantity" + _quantity).show();
    $(".quantity" + _quantity)
      .first()
      .addClass("active");

    var _price = $(".quantity" + _quantity)
      .first()
      .attr("data-price");
    $(".product-price").text(_price);
    var _count = $(".quantity" + _quantity)
      .first()
      .attr("data-count");
    $(".product-count").text(_count);
  });
  // End

  // End

  // Show the price and count according to selected count
  $(".choose-count").on("click", function () {
    $(".choose-count").removeClass("active");
    $(this).addClass("active");

    var _price = $(this).attr("data-price");
    $(".product-price").text(_price);
    var _count = $(this).attr("data-count");
    $(".product-count").text(_count);
  });

  // Show the first selected quantity and its price and count
  $(".choose-quantity").first().addClass("focused");
  var _quantity = $(".choose-quantity").first().attr("data-quantity");
  var _price = $(".quantity" + _quantity)
    .first()
    .attr("data-price");
  var _count = $(".quantity" + _quantity)
    .first()
    .attr("data-count");

  $(".quantity" + _quantity).show();
  $(".quantity" + _quantity)
    .first()
    .addClass("active");
  $(".product-price").text(_price);
  $(".product-count").text(_count);

  // Add to cart
  $(document).on("click", ".add-to-cart", function () {
    var _vm = $(this);
    var _index = _vm.attr("data-index");
    var _qty = $(".product-qty-" + _index).val();
    var _productId = $(".product-id-" + _index).val();
    var _productImage = $(".product-image-" + _index).val();
    var _productTitle = $(".product-title-" + _index).val();
    var _productPrice = $(".product-price-" + _index).text();

    console.log("Price for product ID:", _productId, "is", _productPrice);

    if (_productPrice === "") {
      console.error("Price is empty");
      return;
    }

    // Ajax
    $.ajax({
      url: "/add-to-cart",
      data: {
        id: _productId,
        image: _productImage,
        qty: _qty,
        title: _productTitle,
        price: _productPrice,
      },
      dataType: "json",
      beforeSend: function () {
        _vm.attr("disabled", true);
      },
      success: function (res) {
        $(".cart-list").text(res.totalitems);
        _vm.attr("disabled", false);
      },
      error: function (xhr, status, error) {
        console.error("Error adding to cart:", error);
        _vm.removeClass("added").attr("disabled", false);
      },
    });
    // End
  });
  // End Add to cart

  // Checkout
  $(document).on("click", ".checkout", function () {
    var _vm = $(this);
    console.log("Checkout", _vm);
    // return;
    // Ajax
    $.ajax({
      url: "/checkout",
      dataType: "json",
      beforeSend: function () {
        _vm.attr("disabled", true);
      },
      success: function (res) {
        $(".cart-list").text(res.totalitems);
        _vm.attr("disabled", false);
      },
    });
    // End
  });
  // End Checkout

  // Delete item from cart
  $(document).on("click", ".delete-item", function () {
    var _pId = $(this).attr("data-item");
    var _vm = $(this);
    // Ajax
    $.ajax({
      url: "/delete-from-cart",
      data: {
        id: _pId,
      },
      dataType: "json",
      beforeSend: function () {
        _vm.attr("disabled", true);
      },
      success: function (res) {
        $(".cart-list").text(res.totalitems);
        _vm.attr("disabled", false);
        $("#cartList").html(res.data);
      },
    });
  });

  // Update item from cart
  $(document).on("click", ".update-item", function () {
    var _pId = $(this).attr("data-item");
    var _pQty = $(".product-qty-" + _pId).val();
    var _vm = $(this);
    // Ajax
    $.ajax({
      url: "/update-cart",
      data: {
        id: _pId,
        qty: _pQty,
      },
      dataType: "json",
      beforeSend: function () {
        _vm.attr("disabled", true);
      },
      success: function (res) {
        // $(".cart-list").text(res.totalitems);
        _vm.attr("disabled", false);
        $("#cartList").html(res.data);
      },
    });
    // End
  });
});
