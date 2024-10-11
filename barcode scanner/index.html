<?php
// Configuration
$db_host = 'localhost';
$db_username = 'root';
$db_password = '';
$db_name = 'zapkart_database';

// Create connection
$conn = new mysqli($db_host, $db_username, $db_password, $db_name);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Scan barcode
$barcode = $_POST['barcode'];

// Query to fetch product details
$query = "SELECT * FROM products WHERE barcode = '$barcode'";
$result = $conn->query($query);

if ($result->num_rows > 0) {
    // Output data of each row
    while($row = $result->fetch_assoc()) {
        echo "<table>";
        echo "<tr><th>Product Name</th><td>" . $row["product_name"]. "</td></tr>";
        echo "<tr><th>Quantity</th><td>" . $row["quantity"]. "</td></tr>";
        echo "<tr><th>Price</th><td>" . $row["price"]. "</td></tr>";
        echo "</table>";
    }
} else {
    echo "0 results";
}

$conn->close();
?>

<!-- HTML form to input barcode -->
<form action="<?php echo $_SERVER['PHP_SELF']; ?>" method="post">
    <input type="text" id="barcode" name="barcode" placeholder="Scan barcode" autofocus onkeypress="scanBarcode()">
    <input type="submit" value="Submit">
</form>

<!-- JavaScript code to handle barcode scanning -->
<script>
    function scanBarcode() {
        var barcodeInput = document.getElementById("barcode");
        var barcodeValue = barcodeInput.value;
        if (barcodeValue != "") {
            document.forms[0].submit();
        }
    }
</script>

<!-- Style the table -->
<style>
    table {
        border-collapse: collapse;
        width: 50%;
    }
    th, td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }
</style>