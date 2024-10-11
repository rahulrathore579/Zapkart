<?php
// Database connection
require_once 'db.php';

// Create table
$sql = "CREATE TABLE IF NOT EXISTS products (
    barcode_id INT PRIMARY KEY,
    product_name VARCHAR(255),
    quantity INT,
    price DECIMAL(10, 2)
)";

if ($conn->query($sql) === TRUE) {
    echo "Table created successfully";
} else {
    echo "Error creating table: " . $conn->error;
}

// Insert sample data
$products = array(
    array('barcode_id' => 123456, 'product_name' => 'Product A', 'quantity' => 10, 'price' => 19.99),
    array('barcode_id' => 789012, 'product_name' => 'Product B', 'quantity' => 20, 'price' => 29.99),
    array('barcode_id' => 345678, 'product_name' => 'Product C', 'quantity' => 30, 'price' => 39.99)
);

foreach ($products as $product) {
    $sql = "INSERT INTO products (barcode_id, product_name, quantity, price) VALUES (?, ?, ?, ?)";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("isii", $product['barcode_id'], $product['product_name'], $product['quantity'], $product['price']);
    $stmt->execute();
}

echo "Sample data inserted successfully";

// HTML and JavaScript code
?>
<html>
<head>
    <title>Barcode Scanner</title>
    <style>
        #product-details {
            display: none;
        }
        #product-details table {
            border-collapse: collapse;
            width: 100%;
        }
        #product-details th, #product-details td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        #product-details th {
            background-color: #f0f0f0;
        }
    </style>
</head>
<body>
    <h1>Barcode Scanner</h1>
    <form>
        <input type="text" id="barcode" placeholder="Scan barcode">
        <button type="submit" id="scan-button">Scan</button>
    </form>
    <div id="product-details"></div>

    <script>
        const barcodeInput = document.getElementById('barcode');
        const scanButton = document.getElementById('scan-button');
        const form = document.querySelector('form');
        const productDetailsDiv = document.getElementById('product-details');

        scanButton.addEventListener('click', (e) => {
            e.preventDefault();
            const barcode = barcodeInput.value.trim();
            if (barcode !== '') {
                fetch('index.php', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    body: `barcode=${barcode}`
                })
                .then(response => response.text())
                .then((data) => {
                    productDetailsDiv.innerHTML = data;
                    productDetailsDiv.style.display = 'block';
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
            }
        });
    </script>
</body>
</html>

<?php
// Fetch product data
if (isset($_POST['barcode'])) {
    $barcode = $_POST['barcode'];
    $sql = "SELECT * FROM products WHERE barcode_id = '$barcode'";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        $product = $result->fetch_assoc();
        ?>
        <h2>Product Details</h2>
        <table>
            <tr>
                <th>Barcode ID</th>
                <td><?= $product['barcode_id'] ?></td>
            </tr>
            <tr>
                <th>Product Name</th>
                <td><?= $product['product_name'] ?></td>
            </tr>
            <tr>
                <th>Quantity</th>
                <td><?= $product['quantity'] ?></td>
            </tr>
            <tr>
                <th>Price</th>
                <td><?= $product['price'] ?></td>
            </tr>
        </table>
        <?php
    } else {
        echo "Product not found";
    }
}
?>