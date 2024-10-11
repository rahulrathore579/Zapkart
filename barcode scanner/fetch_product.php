<?php
// fetch_product.php

require_once 'db.php';

if (isset($_POST['barcode'])) {
    $barcode = $_POST['barcode'];
    $sql = "SELECT * FROM products WHERE barcode = '$barcode'";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        $product = $result->fetch_assoc();
        ?>
        <table>
            <tr>
                <th>Product ID</th>
                <td><?= $product['id'] ?></td>
            </tr>
            <tr>
                <th>Product Name</th>
                <td><?= $product['name'] ?></td>
            </tr>
            <tr>
                <th>Price</th>
                <td><?= $product['price'] ?></td>
            </tr>
            <!-- Add more columns as needed -->
        </table>
        <?php
    } else {
        echo "Product not found";
    }
}
?>