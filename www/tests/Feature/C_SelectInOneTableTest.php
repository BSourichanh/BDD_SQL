<?php

use Illuminate\Support\Facades\DB;

test('query-1.sql : liste des produits', function() {
    $result = runQuery(1);
    $this->assertCount(13, $result);
})->skip(!file_exists(dirname(__DIR__)."/../results/queries/query-1.sql"), 'Il manque le fichier query-1.sql');


test('query-2.sql : Liste des produits en rupture de stock (dont la quantité est “0”)', function() {
    $articles = DB::table('products')->get();
    $expected = $articles->filter(function ($article) { return $article->quantity == 0; });

    $result = runQuery(2);
    $this->assertCount($expected->count(), $result);
})->skip(!file_exists(dirname(__DIR__)."/../results/queries/query-2.sql")
    , 'Il manque le fichier query-2.sql');


test('query-3.sql : Liste des commandes d’aujourd’hui classées par n° décroissant', function() {
    $commandes = DB::table('orders')->get();
    $expected = $commandes
        ->filter(function ($commande) { return Carbon\Carbon::parse($commande->date)->isToday(); })
        ->sortByDesc(function ($commande) {
        return $commande->number;
    })->values();

    $result = runQuery(3);
    $this->assertEquals(
        $expected->count(),
        count($result),
        'La requête ne retourne pas le bon nombre de résultats'
    );
    $this->assertEquals(
        $expected->pluck('number'),
        collect($result)->pluck('number'),
        'Les résultats ne sont pas classées par n° décroissant'
    );
})->skip(!file_exists(dirname(__DIR__)."/../results/queries/query-3.sql")
    , 'Il manque le fichier query-3.sql');

test('query-4.sql : Liste des commandes créées depuis les 10 derniers jours', function() {
    $commandes = DB::table('orders')->get();
    $expected = $commandes
        ->filter(function ($commande) { return Carbon\Carbon::parse($commande->date)->diffInDays() < 10; })
        ->values();

    $result = runQuery(4);
    $this->assertEquals(
        $expected->count(),
        count($result),
        'La requête ne retourne pas le bon nombre de résultats'
    );

})->skip(!file_exists(dirname(__DIR__)."/../results/queries/query-4.sql")
    , 'Il manque le fichier query-4.sql');
