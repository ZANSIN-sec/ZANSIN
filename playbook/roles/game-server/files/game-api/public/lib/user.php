<?php
function table_list($row){
    echo "<td>" . htmlspecialchars($row['level'], ENT_QUOTES, "utf-8") . "</td>";
    echo "<td>" . htmlspecialchars($row['stamina'], ENT_QUOTES, "utf-8") . "</td>";
    echo "<td>" . htmlspecialchars($row['gold'], ENT_QUOTES, "utf-8") . "</td>";
    echo "<td>" . htmlspecialchars($row['exp'], ENT_QUOTES, "utf-8") . "</td>";
    echo "<td>" . htmlspecialchars($row['weapon_id'], ENT_QUOTES, "utf-8") . "</td>";
    echo "<td>" . htmlspecialchars($row['armor_id'], ENT_QUOTES, "utf-8") . "</td>";
}