<?php

use Illuminate\Support\Facades\DB;

test('query-5.sql : Liste des produits (nom du produit, quantité et prix unitaire) de la commande portant l\'id 1', function() {
    $orders_and_products = DB::table('order_product')->get();
    $expected = $orders_and_products
        ->filter(function ($op) { return $op->order_id === 1; })
        ->map(function ($op) {
            $product = DB::table('products')
                                            ->where('id', $op->product_id)
                                            ->first();
            return [
                'name' => $product->name,
                'quantity' => $op->quantity,
                'price' => $product->price,
            ];
        })->values()->toArray();

    $results = runQuery(5);
    $this->assertCount(
        count($expected),
        $results,
        'La requête ne retourne pas le bon nombre de résultats'
    );

    foreach ($results as $po) {
        $this->assertObjectHasAttribute('name', $po, "Il manque le nom de l'article");
        $this->assertObjectHasAttribute('quantity', $po, "Il manque la quantité");
        $this->assertObjectHasAttribute('price', $po, "Il manque le prix unitaire");
    }

    $this->assertEquals(
        collect($expected)->map(function ($result) {
            return array_values($result);
        })->toArray(),
        collect($results)->map(function ($result) {
            return array_values(get_object_vars($result));
        })->toArray()
    );

})->skip(!file_exists(dirname(__DIR__)."/../results/queries/query-5.sql")
    , 'Il manque le fichier query-5.sql');

test('query-6.sql : Liste de toutes les commandes : Numéro + Prix total de la commande (calculé sur la base des prix des articles et des quantités de la commande)', function() {
    $expected = getOrdersCollection();

    $results = runQuery(6);

    $this->assertCount(
        DB::table('orders')->count(),
        $expected,
        'Erreur inconnue - vérifiez vos données'
    );
    $this->assertCount(
        DB::table('orders')->count(),
        $results,
        'La requête ne retourne pas le bon nombre de résultats'
    );

    $this->assertEquals(
        prepareOrdersExpected($expected),
        prepareOrdersResults($results)
    );

})->skip(!file_exists(dirname(__DIR__)."/../results/queries/query-6.sql")
    , 'Il manque le fichier query-6.sql');

test('query-7.sql : Montant total des commandes d’aujourd’hui.', function() {
    $expected = getOrdersCollection();
    $result = runQuery(7);

    $this->assertCount(
        1,
        $result,
        'La requête ne doit retourner qu\'une seule ligne'
    );

    $total_expected = $expected->filter(function ($commande) { return Carbon\Carbon::parse($commande['date'])->isToday(); })->sum('total');
    $total_result = (int) array_values(get_object_vars($result[0]))[0];

    $this->assertEquals($total_expected, $total_result);

})->skip(!file_exists(dirname(__DIR__)."/../results/queries/query-7.sql")
    , 'Il manque le fichier query-7.sql');

test('query-8.sql : Liste des commandes dont le prix est compris entre 100 et 550 euros', function() {
    $expected = getOrdersCollection()->filter(function ($commande) {
        return $commande['total'] > 100 && $commande['total'] < 550;
    });
    $results = runQuery(8);

    $this->assertCount(
        $expected->count(),
        $results,
        'La requête ne retourne pas le bon nombre de résultats'
    );

    $this->assertEquals(
        prepareOrdersExpected($expected),
        prepareOrdersResults($results)
    );

})->skip(!file_exists(dirname(__DIR__)."/../results/queries/query-8.sql")
    , 'Il manque le fichier query-8.sql');

test('query-9.sql : Liste des commandes  (Numéro + Prix total de la commande) du client “Charlize”', function() {
    $customer = DB::table('customers')->where('first_name', 'Charlize')->first();
    $expected = getOrdersCollection()->filter(function ($commande) use ($customer) {
        return $commande['customer'] === $customer->id;
    });

    $results = runQuery(9);

    $this->assertCount(
        $expected->count(),
        $results,
        'La requête ne retourne pas le bon nombre de résultats'
    );

    $this->assertEquals(
        prepareOrdersExpected($expected),
        prepareOrdersResults($results)
    );

})->skip(!file_exists(dirname(__DIR__)."/../results/queries/query-9.sql")
    , 'Il manque le fichier query-9.sql');

test('query-10.sql : Nombre de commandes par client (Prénom du client + Nom du client + Nombre de commandes)', function() {
    $customers = DB::table('customers')->orderBy('first_name')->get();
    $orders = DB::table('orders')->get();
    $expected = $customers->map(function ($customer) use ($orders) {
        return [
            $customer->first_name,
            $customer->last_name,
            $orders->where('customer_id', $customer->id)->count()
        ];
    })->toArray();

    $results = runQuery(10);


    $this->assertCount(
        count($expected),
        $customers,
        'La requête ne retourne pas le bon nombre de résultats'
    );

    $results_array = collect($results)->sortBy('first_name')->map(function ($result) {
        return array_values(get_object_vars($result));
    })->values()->toArray();

    $this->assertEquals(
        $expected,
        $results_array
    );
})->skip(!file_exists(dirname(__DIR__)."/../results/queries/query-10.sql")
    , 'Il manque le fichier query-10.sql');

test('query-11.sql : Somme des montants de commandes par client (Prénom du client + Nom du client + Somme des montants de commandes)', function() {
    $customers = DB::table('customers')->orderBy('first_name')->get();
    $orders = getOrdersCollection();
    $expected = $customers->map(function ($customer) use ($orders) {
        return [
            $customer->first_name,
            $customer->last_name,
            $orders->where('customer', $customer->id)->sum('total'),
        ];
    })->toArray();

    $results = runQuery(11);

    $this->assertCount(
        count($expected),
        $customers,
        'La requête ne retourne pas le bon nombre de résultats'
    );

    $results_array = collect($results)->sortBy('first_name')->map(function ($result) {
        $array = array_values(get_object_vars($result));
        return [
            $array[0],
            $array[1],
            (int) $array[2]
        ];
    })->values()->toArray();
    ksort($results_array);

    $this->assertEquals(
        $expected,
        $results_array
    );
})->skip(!file_exists(dirname(__DIR__)."/../results/queries/query-11.sql")
    , 'Il manque le fichier query-11.sql');
