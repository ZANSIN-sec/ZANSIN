use miniquest;

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

CREATE TABLE `battle_history` (
                                  `id` int(10) UNSIGNED NOT NULL,
                                  `user_id` int(11) NOT NULL,
                                  `enemy_id` int(11) NOT NULL,
                                  `course_id` int(11) NOT NULL,
                                  `result` varchar(1024) NOT NULL,
                                  `turn_count` int(11) NOT NULL,
                                  `total_damage` int(11) NOT NULL,
                                  `get_exp` int(11) NOT NULL,
                                  `get_gold` int(11) NOT NULL,
                                  `created_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `course` (
                          `id` int(11) NOT NULL,
                          `name` varchar(1024) NOT NULL,
                          `stamina` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `course` (`id`, `name`, `stamina`) VALUES
(1, 'easy', 10),
(2, 'normal', 20),
(3, 'hard', 30),
(4, 'very hard', 40),
(5, 'nightmare', 50),
(6, 'test', 1);

CREATE TABLE `enemy` (
                         `id` int(10) UNSIGNED NOT NULL,
                         `hp` int(11) NOT NULL,
                         `str` int(11) NOT NULL,
                         `course_id` int(11) NOT NULL,
                         `gold` int(11) NOT NULL,
                         `exp` int(11) NOT NULL,
                         `name` varchar(1024) NOT NULL,
                         `image` varchar(1024) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `enemy` (`id`, `hp`, `str`, `course_id`, `gold`, `exp`, `name`, `image`) VALUES
(1, 15, 4, 1, 1, 1, 'Nomal Slime', 'enemy001.png'),
(2, 50, 13, 2, 5, 2, 'Powerful Slime', 'enemy002.png'),
(3, 151, 40, 3, 25, 4, 'Muscular Slime', 'enemy003.png'),
(4, 503, 133, 4, 125, 8, 'Awesomely Strong Slime', 'enemy004.png'),
(5, 1677, 443, 5, 625, 16, 'Devilish Slime', 'enemy005.png'),
(6, 1, 1, 6, 500, 500, 'Test Slime', 'enemy099.png');

CREATE TABLE `equipment` (
                             `id` int(10) UNSIGNED NOT NULL,
                             `type` varchar(1024) NOT NULL,
                             `rarity` varchar(1024) NOT NULL,
                             `name` varchar(1024) NOT NULL,
                             `param` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `equipment` (`id`, `type`, `rarity`, `name`, `param`) VALUES
(1, 'any', 'init', 'None', 0),
(2, 'weapon', 'N', 'Cypress Stick', 3),
(3, 'weapon', 'N', 'Bamboo Sword', 6),
(4, 'weapon', 'N', 'Wooden Sword', 9),
(5, 'weapon', 'N', 'Stone Axe', 12),
(6, 'weapon', 'N', 'Bronze Sword', 15),
(7, 'weapon', 'N', 'Iron Axe', 18),
(8, 'weapon', 'N', 'Rapier', 21),
(9, 'weapon', 'N', 'Iron Lance', 24),
(10, 'weapon', 'R', 'Steel Broadsword', 30),
(11, 'weapon', 'R', 'Morning Star', 35),
(12, 'weapon', 'R', 'Chinese sword', 40),
(13, 'weapon', 'R', 'Samurai Sword', 45),
(14, 'weapon', 'R', 'The Unnamable Crowbar', 50),
(15, 'weapon', 'SR', 'Masamune', 70),
(16, 'weapon', 'SR', 'Legendary Holy Sword', 80),
(17, 'armor', 'N', 'Plain Clothes', 3),
(18, 'armor', 'N', 'Boxer Shorts', 6),
(19, 'armor', 'N', 'Leather Armour', 9),
(20, 'armor', 'N', 'Pirate Clothes', 12),
(21, 'armor', 'N', 'Chain Mail', 15),
(22, 'armor', 'N', 'Bronze Armour', 18),
(23, 'armor', 'N', 'Bulletproof Vest', 21),
(24, 'armor', 'N', 'Iron Cuirass', 24),
(25, 'armor', 'R', 'Full Plate Armour', 30),
(26, 'armor', 'R', 'Gold Armour', 35),
(27, 'armor', 'R', 'Stealth Suit', 40),
(28, 'armor', 'R', 'Wandering Armor', 45),
(29, 'armor', 'R', 'Samulai Armor', 50),
(30, 'armor', 'SR', 'Sage Robe', 70),
(31, 'armor', 'SR', 'Legendary Holy Armor', 80);

CREATE TABLE `level` (
                         `level` int(10) UNSIGNED NOT NULL,
                         `max_hp` int(11) NOT NULL,
                         `max_str` int(11) NOT NULL,
                         `max_stamina` int(11) NOT NULL,
                         `need_exp` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `level` (`level`, `max_hp`, `max_str`, `max_stamina`, `need_exp`) VALUES
(1, 15, 5, 10, 2),
(2, 17, 6, 12, 2),
(3, 19, 7, 13, 2),
(4, 21, 8, 15, 2),
(5, 23, 9, 16, 2),
(6, 25, 10, 18, 3),
(7, 27, 11, 19, 3),
(8, 29, 12, 21, 3),
(9, 31, 13, 22, 3),
(10, 33, 14, 24, 3),
(11, 35, 15, 25, 3),
(12, 37, 16, 27, 3),
(13, 39, 17, 28, 4),
(14, 41, 18, 30, 4),
(15, 43, 19, 31, 4),
(16, 45, 20, 33, 4),
(17, 47, 21, 34, 4),
(18, 49, 22, 36, 5),
(19, 51, 23, 37, 5),
(20, 53, 24, 39, 5),
(21, 55, 25, 40, 5),
(22, 57, 26, 42, 6),
(23, 59, 27, 43, 6),
(24, 61, 28, 45, 6),
(25, 63, 29, 46, 6),
(26, 65, 30, 48, 7),
(27, 67, 31, 49, 7),
(28, 69, 32, 51, 7),
(29, 71, 33, 52, 8),
(30, 73, 34, 54, 8),
(31, 75, 35, 55, 9),
(32, 77, 36, 57, 9),
(33, 79, 37, 58, 10),
(34, 81, 38, 60, 10),
(35, 83, 39, 61, 11),
(36, 85, 40, 63, 11),
(37, 87, 41, 64, 12),
(38, 89, 42, 66, 12),
(39, 91, 43, 67, 13),
(40, 93, 44, 69, 13),
(41, 95, 45, 70, 14),
(42, 97, 46, 72, 15),
(43, 99, 47, 73, 16),
(44, 101, 48, 75, 16),
(45, 103, 49, 76, 17),
(46, 105, 50, 78, 18),
(47, 107, 51, 79, 19),
(48, 109, 52, 81, 20),
(49, 111, 53, 82, 21),
(50, 113, 54, 84, 22),
(51, 115, 55, 85, 23),
(52, 117, 56, 87, 24),
(53, 119, 57, 88, 25),
(54, 121, 58, 90, 27),
(55, 123, 59, 91, 28),
(56, 125, 60, 93, 29),
(57, 127, 61, 94, 31),
(58, 129, 62, 96, 32),
(59, 131, 63, 97, 34),
(60, 133, 64, 99, 36),
(61, 135, 65, 100, 37),
(62, 137, 66, 102, 39),
(63, 139, 67, 103, 41),
(64, 141, 68, 105, 43),
(65, 143, 69, 106, 45),
(66, 145, 70, 108, 48),
(67, 147, 71, 109, 50),
(68, 149, 72, 111, 53),
(69, 151, 73, 112, 55),
(70, 153, 74, 114, 58),
(71, 155, 75, 115, 61),
(72, 157, 76, 117, 64),
(73, 159, 77, 118, 67),
(74, 161, 78, 120, 70),
(75, 163, 79, 121, 74),
(76, 165, 80, 123, 78),
(77, 167, 81, 124, 82),
(78, 169, 82, 126, 86),
(79, 171, 83, 127, 90),
(80, 173, 84, 129, 94),
(81, 175, 85, 130, 99),
(82, 177, 86, 132, 104),
(83, 179, 87, 133, 109),
(84, 181, 88, 135, 115),
(85, 183, 89, 136, 120),
(86, 185, 90, 138, 127),
(87, 187, 91, 139, 133),
(88, 189, 92, 141, 139),
(89, 191, 93, 142, 146),
(90, 193, 94, 144, 154),
(91, 195, 95, 145, 161),
(92, 197, 96, 147, 170),
(93, 199, 97, 148, 178),
(94, 201, 98, 150, 187),
(95, 203, 99, 151, 196),
(96, 205, 100, 153, 206),
(97, 207, 101, 154, 216),
(98, 209, 102, 156, 227),
(99, 211, 103, 157, 239);

CREATE TABLE `player` (
                          `id` int(10) UNSIGNED NOT NULL,
                          `user_name` varchar(1024) NOT NULL,
                          `password` varchar(1024) NOT NULL,
                          `nick_name` varchar(1024) NOT NULL,
                          `image` varchar(1024) NOT NULL,
                          `level` int(11) NOT NULL,
                          `stamina` int(11) NOT NULL,
                          `weapon_id` int(11) NOT NULL,
                          `armor_id` int(11) NOT NULL,
                          `gold` int(11) NOT NULL,
                          `exp` int(11) NOT NULL,
                          `created_at` datetime NOT NULL,
                          `staminaupdated_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE `battle_history`
    ADD PRIMARY KEY (`id`);

ALTER TABLE `course`
    ADD PRIMARY KEY (`id`);

ALTER TABLE `enemy`
    ADD PRIMARY KEY (`id`);

ALTER TABLE `equipment`
    ADD PRIMARY KEY (`id`);

ALTER TABLE `level`
    ADD PRIMARY KEY (`level`);

ALTER TABLE `player`
    ADD PRIMARY KEY (`id`);

ALTER TABLE `battle_history`
    MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

ALTER TABLE `course`
    MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=100;

ALTER TABLE `enemy`
    MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

ALTER TABLE `equipment`
    MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

ALTER TABLE `level`
    MODIFY `level` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=100;

ALTER TABLE `player`
    MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;
