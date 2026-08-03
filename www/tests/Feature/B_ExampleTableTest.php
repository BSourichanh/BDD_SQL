<?php

test('Requête de test', function () {
    $result = runQuery(0);
    $this->assertCount(1, $result);
    expect($result[0]->name)->toEqual('Campus Numérique In The Alps');
});
