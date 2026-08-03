<?php

test("Présence de la table 'categories'", function() {
    expect(hasTable('categories'))->toBeTrue();
})->skip(file_exists(dirname(__DIR__) . "../results/database/dump.sql"), 'La table `categories` est manquante');

test("Présence de la table 'customers'", function() {
    expect(hasTable('customers'))->toBeTrue();
})->skip(file_exists(dirname(__DIR__) . "../results/database/dump.sql"), 'La table `customers` est manquante');

test("Présence de la table 'order_product'", function() {
    expect(hasTable('order_product'))->toBeTrue();
})->skip(file_exists(dirname(__DIR__) . "../results/database/dump.sql"), 'La table `order_product` est manquante');

test("Présence de la table 'orders'", function() {
    expect(hasTable('orders'))->toBeTrue();
})->skip(file_exists(dirname(__DIR__) . "../results/database/dump.sql"), 'La table `orders` est manquante');

test("Présence du numéro de commande dans la table 'orders'", function() {
    expect(tableHasColumn('orders', 'number'))->toBeTrue();
})->skip(file_exists(dirname(__DIR__) . "../results/database/dump.sql"), 'La table `orders` doit contenir le champ `number`');

test("Présence du champ `customer_id` dans la table 'orders'", function() {
    expect(tableHasColumn('orders', 'customer_id'))->toBeTrue();
})->skip(file_exists(dirname(__DIR__) . "../results/database/dump.sql"), 'La table `orders` doit contenir le champ `customer_id`');

test("Présence de la date de commande dans la table 'orders'", function() {
    expect(tableHasColumn('orders', 'date'))->toBeTrue();
})->skip(file_exists(dirname(__DIR__) . "../results/database/dump.sql"), 'La table `orders` doit contenir le champ `date`');

test("Présence de la table 'products'", function() {
    expect(hasTable('products'))->toBeTrue();
})->skip(file_exists(dirname(__DIR__) . "../results/database/dump.sql"), 'La table `products` est manquante');
