<?php
  $servername = "localhost";
  $username = "root";
  $password = "";
  $dbname = "products";

  // Create connection
  $conn = new mysqli($servername, $username, $password, $dbname);

  // Check connection
  if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
  }

  $barcode = $_POST['barcode'];

  $sql = "SELECT * FROM products WHERE barcode_id = '$barcode'";
  $result = $conn->query($sql);

  if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {
      $product = array(
        'barcode_id' => $row['barcode_id'],
        'product_name' => $row['product_name'],
        'quantity' => $row['quantity'],
        'price' => $row['price']
      );
      echo json_encode($product);
    }
  } else {
    echo "0";
  }

  $conn->close();
?>