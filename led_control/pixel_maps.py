from adafruit_led_animation import helper


class KTPixelMap(helper.PixelMap):
    def __init__(self, strip, pixel_ranges, individual_pixels=False):
        helper.PixelMap.__init__(strip, pixel_ranges, individual_pixels)


    """
    p1_pixel_map_strips = [
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

    p2_pixel_map_strips = [
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

    """
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
        (0, 360, 361)
    ]

    p2_pixel_map_strips = [
        (541,895,896),(542,894,897),(543,893,898),(544,892,899),(545,891,900),(546,890,901),(547,889,902),(548,888,903),(549,887,904),(550,886,905),(551,885,906),(552,884,907),(553,883,908),(554,882,909),(555,881,910),(556,880,911),(557,879,912),(558,878,913),(559,877,914),(560,876,915),(561,875,916),(562,874,917),(563,873,918),(564,872,919),(565,871,920),(566,870,921),(567,869,922),(568,868,923),(569,867,924),(570,866,925),(571,865,926),(572,864,927),(573,863,928),(574,862,929),(575,861,930),(576,860,931),(577,859,932),(578,858,933),(579,857,934),(580,856,935),(581,855,936),(582,854,937),(583,853,938),(584,852,939),(585,851,940),(586,850,941),(587,849,942),(588,848,943),(589,847,944),(590,846,945),(591,845,946),(592,844,947),(593,843,948),(594,842,949),(595,841,950),(596,840,951),(597,839,952),(598,838,953),(599,837,954),(600,836,955),(601,835,956),(602,834,957),(603,833,958),(604,832,959),(605,831,960),(606,830,961),(607,829,962),(608,828,963),(609,827,964),(610,826,965),(611,825,966),(612,824,967),(613,823,968),(614,822,969),(615,821,970),(616,820,971),(617,819,972),(618,818,973),(619,817,974),(620,816,975),(621,815,976),(622,814,977),(623,813,978),(624,812,979),(625,811,980),(626,810,981),(627,809,982),(628,808,983),(629,807,984),(630,806,985),(631,805,986),(632,804,987),(633,803,988),(634,802,989),(635,801,990),(636,800,991),(637,799,992),(638,798,993),(639,797,994),(640,796,995),(641,795,996),(642,794,997),(643,793,998),(644,792,999),(645,791,1000),(646,790,1001),(647,789,1002),(648,788,1003),(649,787,1004),(650,786,1005),(651,785,1006),(652,784,1007),(653,783,1008),(654,782,1009),(655,781,1010),(656,780,1011),(657,779,1012),(658,778,1013),(659,777,1014),(660,776,1015),(661,775,1016),(662,774,1017),(663,773,1018),(664,772,1019),(665,771,1020),(666,770,1021),(667,769,1022),(668,768,1023),(669,767,1024),(670,766,1025),(671,765,1026),(672,764,1027),(673,763,1028),(674,762,1029),(675,761,1030),(676,760,1031),(677,759,1032),(678,758,1033),(679,757,1034),(680,756,1035),(681,755,1036),(682,754,1037),(683,753,1038),(684,752,1039),(685,751,1040),(686,750,1041),(687,749,1042),(688,748,1043),(689,747,1044),(690,746,1045),(691,745,1046),(692,744,1047),(693,743,1048),(694,742,1049),(695,741,1050),(696,740,1051),(697,739,1052),(698,738,1053),(699,737,1054),(700,736,1055),(701,735,1056),(702,734,1057),(703,733,1058),(704,732,1059),(705,731,1060),(706,730,1061),(707,729,1062),(708,728,1063),(709,727,1064),(710,726,1065),(711,725,1066),(712,724,1067),(713,723,1068),(714,722,1069),(715,721,1070),(716,720,1071),(717,719,1072),(718,718,1073),(719,717,1074),(720,716,1075)
    ]

