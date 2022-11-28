from adafruit_led_animation import helper


class KTPixelMap(helper.PixelMap):
    def __init__(self, strip, pixel_ranges, individual_pixels=False):
        helper.PixelMap.__init__(strip, pixel_ranges, individual_pixels)

    p1_pixel_map = [
        (255, 254, 253, 252),
        (240, 241, 242, 243),
        (239, 238, 237, 236),
        (224, 225, 226, 227),
        (223, 222, 221, 220),
        (208, 209, 210, 211),
        (207, 206, 205, 204),
        (192, 193, 194, 195),
        (191, 190, 189, 188),
        (176, 177, 178, 179),
        (175, 174, 173, 172),
        (160, 161, 162, 163),
        (159, 158, 157, 156),
        (144, 145, 146, 147),
        (143, 142, 141, 140),
        (128, 129, 130, 131),
        (127, 126, 125, 124),
        (112, 113, 114, 115),
        (111, 110, 109, 108),
        (96, 97, 98, 99),
        (95, 94, 93, 92),
        (80, 81, 82, 83),
        (79, 78, 77, 76),
        (64, 65, 66, 67),
        (63, 62, 61, 60),
        (48, 49, 50, 51),
        (47, 46, 45, 44),
        (32, 33, 34, 35),
        (31, 30, 29, 28),
        (16, 17, 18, 19),
        (15, 14, 13, 12),
        (0, 1, 2, 3),
    ]

    p2_pixel_map = [
        (251, 250, 249, 248),
        (244, 245, 246, 247),
        (235, 234, 233, 232),
        (228, 229, 230, 231),
        (219, 218, 217, 216),
        (212, 213, 214, 215),
        (203, 202, 201, 200),
        (196, 197, 198, 199),
        (187, 186, 185, 184),
        (180, 181, 182, 183),
        (171, 170, 169, 168),
        (164, 165, 166, 167),
        (155, 154, 153, 152),
        (148, 149, 150, 151),
        (139, 138, 137, 136),
        (132, 133, 134, 135),
        (123, 122, 121, 120),
        (116, 117, 118, 119),
        (107, 106, 105, 104),
        (100, 101, 102, 103),
        (91, 90, 89, 88),
        (84, 85, 86, 87),
        (75, 74, 73, 72),
        (68, 69, 70, 71),
        (59, 58, 57, 56),
        (52, 53, 54, 55),
        (43, 42, 41, 40),
        (36, 37, 38, 39),
        (27, 26, 25, 24),
        (20, 21, 22, 23),
        (11, 10, 9, 8),
        (4, 5, 6, 7),
    ]

    p1_pixel_map_strips = [
        (179, 181, 540),
        (178, 182, 539),
        (177, 183, 538),
        (176, 184, 537),
        (175, 185, 536),
        (174, 186, 535),
        (173, 187, 534),
        (172, 188, 533),
        (171, 189, 532),
        (170, 190, 531),
        (169, 191, 530),
        (168, 192, 529),
        (167, 193, 528),
        (166, 194, 527),
        (165, 195, 526),
        (164, 196, 525),
        (163, 197, 524),
        (162, 198, 523),
        (161, 199, 522),
        (160, 200, 521),
        (159, 201, 520),
        (158, 202, 519),
        (157, 203, 518),
        (156, 204, 517),
        (155, 205, 516),
        (154, 206, 515),
        (153, 207, 514),
        (152, 208, 513),
        (151, 209, 512),
        (150, 210, 511),
        (149, 211, 510),
        (148, 212, 509),
        (147, 213, 508),
        (146, 214, 507),
        (145, 215, 506),
        (144, 216, 505),
        (143, 217, 504),
        (142, 218, 503),
        (141, 219, 502),
        (140, 220, 501),
        (139, 221, 500),
        (138, 222, 499),
        (137, 223, 498),
        (136, 224, 497),
        (135, 225, 496),
        (134, 226, 495),
        (133, 227, 494),
        (132, 228, 493),
        (131, 229, 492),
        (130, 230, 491),
        (129, 231, 490),
        (128, 232, 489),
        (127, 233, 488),
        (126, 234, 487),
        (125, 235, 486),
        (124, 236, 485),
        (123, 237, 484),
        (122, 238, 483),
        (121, 239, 482),
        (120, 240, 481),
        (119, 241, 480),
        (118, 242, 479),
        (117, 243, 478),
        (116, 244, 477),
        (115, 245, 476),
        (114, 246, 475),
        (113, 247, 474),
        (112, 248, 473),
        (111, 249, 472),
        (110, 250, 471),
        (109, 251, 470),
        (108, 252, 469),
        (107, 253, 468),
        (106, 254, 467),
        (105, 255, 466),
        (104, 256, 465),
        (103, 257, 464),
        (102, 258, 463),
        (101, 259, 462),
        (100, 260, 461),
        (99, 261, 460),
        (98, 262, 459),
        (97, 263, 458),
        (96, 264, 457),
        (95, 265, 456),
        (94, 266, 455),
        (93, 267, 454),
        (92, 268, 453),
        (91, 269, 452),
        (90, 270, 451),
        (89, 271, 450),
        (88, 272, 449),
        (87, 273, 448),
        (86, 274, 447),
        (85, 275, 446),
        (84, 276, 445),
        (83, 277, 444),
        (82, 278, 443),
        (81, 279, 442),
        (80, 280, 441),
        (79, 281, 440),
        (78, 282, 439),
        (77, 283, 438),
        (76, 284, 437),
        (75, 285, 436),
        (74, 286, 435),
        (73, 287, 434),
        (72, 288, 433),
        (71, 289, 432),
        (70, 290, 431),
        (69, 291, 430),
        (68, 292, 429),
        (67, 293, 428),
        (66, 294, 427),
        (65, 295, 426),
        (64, 296, 425),
        (63, 297, 424),
        (62, 298, 423),
        (61, 299, 422),
        (60, 300, 421),
        (59, 301, 420),
        (58, 302, 419),
        (57, 303, 418),
        (56, 304, 417),
        (55, 305, 416),
        (54, 306, 415),
        (53, 307, 414),
        (52, 308, 413),
        (51, 309, 412),
        (50, 310, 411),
        (49, 311, 410),
        (48, 312, 409),
        (47, 313, 408),
        (46, 314, 407),
        (45, 315, 406),
        (44, 316, 405),
        (43, 317, 404),
        (42, 318, 403),
        (41, 319, 402),
        (40, 320, 401),
        (39, 321, 400),
        (38, 322, 399),
        (37, 323, 398),
        (36, 324, 397),
        (35, 325, 396),
        (34, 326, 395),
        (33, 327, 394),
        (32, 328, 393),
        (31, 329, 392),
        (30, 330, 391),
        (29, 331, 390),
        (28, 332, 389),
        (27, 333, 388),
        (26, 334, 387),
        (25, 335, 386),
        (24, 336, 385),
        (23, 337, 384),
        (22, 338, 383),
        (21, 339, 382),
        (20, 340, 381),
        (19, 341, 380),
        (18, 342, 379),
        (17, 343, 378),
        (16, 344, 377),
        (15, 345, 376),
        (14, 346, 375),
        (13, 347, 374),
        (12, 348, 373),
        (11, 349, 372),
        (10, 350, 371),
        (9, 351, 370),
        (8, 352, 369),
        (7, 353, 368),
        (6, 354, 367),
        (5, 355, 366),
        (4, 356, 365),
        (3, 357, 364),
        (2, 358, 363),
        (1, 359, 362),
        (0, 360, 361),
    ]

    p2_pixel_map_strips = [
        (542, 901, 902),
        (543, 900, 903),
        (544, 899, 904),
        (545, 898, 905),
        (546, 897, 906),
        (547, 896, 907),
        (548, 895, 908),
        (549, 894, 909),
        (550, 893, 910),
        (551, 892, 911),
        (552, 891, 912),
        (553, 890, 913),
        (554, 889, 914),
        (555, 888, 915),
        (556, 887, 916),
        (557, 886, 917),
        (558, 885, 918),
        (559, 884, 919),
        (560, 883, 920),
        (561, 882, 921),
        (562, 881, 922),
        (563, 880, 923),
        (564, 879, 924),
        (565, 878, 925),
        (566, 877, 926),
        (567, 876, 927),
        (568, 875, 928),
        (569, 874, 929),
        (570, 873, 930),
        (571, 872, 931),
        (572, 871, 932),
        (573, 870, 933),
        (574, 869, 934),
        (575, 868, 935),
        (576, 867, 936),
        (577, 866, 937),
        (578, 865, 938),
        (579, 864, 939),
        (580, 863, 940),
        (581, 862, 941),
        (582, 861, 942),
        (583, 860, 943),
        (584, 859, 944),
        (585, 858, 945),
        (586, 857, 946),
        (587, 856, 947),
        (588, 855, 948),
        (589, 854, 949),
        (590, 853, 950),
        (591, 852, 951),
        (592, 851, 952),
        (593, 850, 953),
        (594, 849, 954),
        (595, 848, 955),
        (596, 847, 956),
        (597, 846, 957),
        (598, 845, 958),
        (599, 844, 959),
        (600, 843, 960),
        (601, 842, 961),
        (602, 841, 962),
        (603, 840, 963),
        (604, 839, 964),
        (605, 838, 965),
        (606, 837, 966),
        (607, 836, 967),
        (608, 835, 968),
        (609, 834, 969),
        (610, 833, 970),
        (611, 832, 971),
        (612, 831, 972),
        (613, 830, 973),
        (614, 829, 974),
        (615, 828, 975),
        (616, 827, 976),
        (617, 826, 977),
        (618, 825, 978),
        (619, 824, 979),
        (620, 823, 980),
        (621, 822, 981),
        (622, 821, 982),
        (623, 820, 983),
        (624, 819, 984),
        (625, 818, 985),
        (626, 817, 986),
        (627, 816, 987),
        (628, 815, 988),
        (629, 814, 989),
        (630, 813, 990),
        (631, 812, 991),
        (632, 811, 992),
        (633, 810, 993),
        (634, 809, 994),
        (635, 808, 995),
        (636, 807, 996),
        (637, 806, 997),
        (638, 805, 998),
        (639, 804, 999),
        (640, 803, 1000),
        (641, 802, 1001),
        (642, 801, 1002),
        (643, 800, 1003),
        (644, 799, 1004),
        (645, 798, 1005),
        (646, 797, 1006),
        (647, 796, 1007),
        (648, 795, 1008),
        (649, 794, 1009),
        (650, 793, 1010),
        (651, 792, 1011),
        (652, 791, 1012),
        (653, 790, 1013),
        (654, 789, 1014),
        (655, 788, 1015),
        (656, 787, 1016),
        (657, 786, 1017),
        (658, 785, 1018),
        (659, 784, 1019),
        (660, 783, 1020),
        (661, 782, 1021),
        (662, 781, 1022),
        (663, 780, 1023),
        (664, 779, 1024),
        (665, 778, 1025),
        (666, 777, 1026),
        (667, 776, 1027),
        (668, 775, 1028),
        (669, 774, 1029),
        (670, 773, 1030),
        (671, 772, 1031),
        (672, 771, 1032),
        (673, 770, 1033),
        (674, 769, 1034),
        (675, 768, 1035),
        (676, 767, 1036),
        (677, 766, 1037),
        (678, 765, 1038),
        (679, 764, 1039),
        (680, 763, 1040),
        (681, 762, 1041),
        (682, 761, 1042),
        (683, 760, 1043),
        (684, 759, 1044),
        (685, 758, 1045),
        (686, 757, 1046),
        (687, 756, 1047),
        (688, 755, 1048),
        (689, 754, 1049),
        (690, 753, 1050),
        (691, 752, 1051),
        (692, 751, 1052),
        (693, 750, 1053),
        (694, 749, 1054),
        (695, 748, 1055),
        (696, 747, 1056),
        (697, 746, 1057),
        (698, 745, 1058),
        (699, 744, 1059),
        (700, 743, 1060),
        (701, 742, 1061),
        (702, 741, 1062),
        (703, 740, 1063),
        (704, 739, 1064),
        (705, 738, 1065),
        (706, 737, 1066),
        (707, 736, 1067),
        (708, 735, 1068),
        (709, 734, 1069),
        (710, 733, 1070),
        (711, 732, 1071),
        (712, 731, 1072),
        (713, 730, 1073),
        (714, 729, 1074),
        (715, 728, 1075),
        (716, 727, 1076),
        (717, 726, 1077),
        (718, 725, 1078),
        (719, 724, 1079),
        (720, 723, 1080),
        (721, 722, 1081),
    ]
