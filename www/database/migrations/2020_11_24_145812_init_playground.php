<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;
use Illuminate\Support\Facades\DB;

class InitPlayground extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('sql_playground_test', function (Blueprint $table) {
            $table->id();
            $table->text('name');
            $table->timestamps();
        });
        DB::table('sql_playground_test')->insert([
           'name' => 'Campus Numérique In The Alps'
        ]);

        $file = __DIR__ . '/../../results/database/dump.sql';
        $sql = file_get_contents($file);

        DB::unprepared($sql);
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        DB::connection(DB::getDefaultConnection())
          ->getSchemaBuilder()
          ->dropAllTables();
    }
}
