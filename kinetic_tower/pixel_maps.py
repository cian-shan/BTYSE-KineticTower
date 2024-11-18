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
        (179,180,529),(178,181,529),(177,182,529),(176,183,529),(175,184,529),(174,185,528),(173,186,527),(172,187,526),(171,188,525),(170,189,524),(169,190,523),(168,191,522),(167,192,521),(166,193,520),(165,194,519),(164,195,518),(163,196,517),(162,197,516),(161,198,515),(160,199,514),(159,200,513),(158,201,512),(157,202,511),(156,203,510),(155,204,509),(154,205,508),(153,206,507),(152,207,506),(151,208,505),(150,209,504),(149,210,503),(148,211,502),(147,212,501),(146,213,500),(145,214,499),(144,215,498),(143,216,497),(142,217,496),(141,218,495),(140,219,494),(139,220,493),(138,221,492),(137,222,491),(136,223,490),(135,224,489),(134,225,488),(133,226,487),(132,227,486),(131,228,485),(130,229,484),(129,230,483),(128,231,482),(127,232,481),(126,233,480),(125,234,479),(124,235,478),(123,236,477),(122,237,476),(121,238,475),(120,239,474),(119,240,473),(118,241,472),(117,242,471),(116,243,470),(115,244,469),(114,245,468),(113,246,467),(112,247,466),(111,248,465),(110,249,464),(109,250,463),(108,251,462),(107,252,461),(106,253,460),(105,254,459),(104,255,458),(103,256,457),(102,257,456),(101,258,455),(100,259,454),(99,260,453),(98,261,452),(97,262,451),(96,263,450),(95,264,449),(94,265,448),(93,266,447),(92,267,446),(91,268,445),(90,269,444),(89,270,443),(88,271,442),(87,272,441),(86,273,440),(85,274,439),(84,275,438),(83,276,437),(82,277,436),(81,278,435),(80,279,434),(79,280,433),(78,281,432),(77,282,431),(76,283,430),(75,284,429),(74,285,428),(73,286,427),(72,287,426),(71,288,425),(70,289,424),(69,290,423),(68,291,422),(67,292,421),(66,293,420),(65,294,419),(64,295,418),(63,296,417),(62,297,416),(61,298,415),(60,299,414),(59,300,413),(58,301,412),(57,302,411),(56,303,410),(55,304,409),(54,305,408),(53,306,407),(52,307,406),(51,308,405),(50,309,404),(49,310,403),(48,311,402),(47,312,401),(46,313,400),(45,314,399),(44,315,398),(43,316,397),(42,317,396),(41,318,395),(40,319,394),(39,320,393),(38,321,392),(37,322,391),(36,323,390),(35,324,389),(34,325,388),(33,326,387),(32,327,386),(31,328,385),(30,329,384),(29,330,383),(28,331,382),(27,332,381),(26,333,380),(25,334,379),(24,335,378),(23,336,377),(22,337,376),(21,338,375),(20,339,374),(19,340,373),(18,341,372),(17,342,371),(16,343,370),(15,344,369),(14,345,368),(13,346,367),(12,347,366),(11,348,365),(10,349,364),(9,350,363),(8,351,362),(7,352,361),(6,353,360),(5,354,359),(4,355,358),(3,356,357),(2,357,356),(1,358,355),(0,359,354),
    ]


    p2_pixel_map_strips = [
        (530,884,885),(531,883,886),(532,882,887),(533,881,888),(534,880,889),(535,879,890),(536,878,891),(537,877,892),(538,876,893),(539,875,894),(540,874,895),(541,873,896),(542,872,897),(543,871,898),(544,870,899),(545,869,900),(546,868,901),(547,867,902),(548,866,903),(549,865,904),(550,864,905),(551,863,906),(552,862,907),(553,861,908),(554,860,909),(555,859,910),(556,858,911),(557,857,912),(558,856,913),(559,855,914),(560,854,915),(561,853,916),(562,852,917),(563,851,918),(564,850,919),(565,849,920),(566,848,921),(567,847,922),(568,846,923),(569,845,924),(570,844,925),(571,843,926),(572,842,927),(573,841,928),(574,840,929),(575,839,930),(576,838,931),(577,837,932),(578,836,933),(579,835,934),(580,834,935),(581,833,936),(582,832,937),(583,831,938),(584,830,939),(585,829,940),(586,828,941),(587,827,942),(588,826,943),(589,825,944),(590,824,945),(591,823,946),(592,822,947),(593,821,948),(594,820,949),(595,819,950),(596,818,951),(597,817,952),(598,816,953),(599,815,954),(600,814,955),(601,813,956),(602,812,957),(603,811,958),(604,810,959),(605,809,960),(606,808,961),(607,807,962),(608,806,963),(609,805,964),(610,804,965),(611,803,966),(612,802,967),(613,801,968),(614,800,969),(615,799,970),(616,798,971),(617,797,972),(618,796,973),(619,795,974),(620,794,975),(621,793,976),(622,792,977),(623,791,978),(624,790,979),(625,789,980),(626,788,981),(627,787,982),(628,786,983),(629,785,984),(630,784,985),(631,783,986),(632,782,987),(633,781,988),(634,780,989),(635,779,990),(636,778,991),(637,777,992),(638,776,993),(639,775,994),(640,774,995),(641,773,996),(642,772,997),(643,771,998),(644,770,999),(645,769,1000),(646,768,1001),(647,767,1002),(648,766,1003),(649,765,1004),(650,764,1005),(651,763,1006),(652,762,1007),(653,761,1008),(654,760,1009),(655,759,1010),(656,758,1011),(657,757,1012),(658,756,1013),(659,755,1014),(660,754,1015),(661,753,1016),(662,752,1017),(663,751,1018),(664,750,1019),(665,749,1020),(666,748,1021),(667,747,1022),(668,746,1023),(669,745,1024),(670,744,1025),(671,743,1026),(672,742,1027),(673,741,1028),(674,740,1029),(675,739,1030),(676,738,1031),(677,737,1032),(678,736,1033),(679,735,1034),(680,734,1035),(681,733,1036),(682,732,1037),(683,731,1038),(684,730,1039),(685,729,1040),(686,728,1041),(687,727,1042),(688,726,1043),(689,725,1044),(690,724,1045),(691,723,1046),(692,722,1047),(693,721,1048),(694,720,1049),(695,719,1050),(696,718,1051),(697,717,1052),(698,716,1053),(699,715,1054),(700,714,1055),(701,713,1056),(702,712,1057),(703,711,1058),(704,710,1059),(705,709,1060),(706,708,1061),(707,707,1062),(708,706,1063),(709,705,1064),

    ]
    
    combined_pixel_map = [
        (179,180,529,530,884,885),
        (178,181,529,531,883,886),
        (177,182,529,532,882,887),
        (176,183,529,533,881,888),
        (175,184,529,534,880,889),
        (174,185,528,535,879,890),
        (173,186,527,536,878,891),
        (172,187,526,537,877,892),
        (171,188,525,538,876,893),
        (170,189,524,539,875,894),
        (169,190,523,540,874,895),
        (168,191,522,541,873,896),
        (167,192,521,542,872,897),
        (166,193,520,543,871,898),
        (165,194,519,544,870,899),
        (164,195,518,545,869,900),
        (163,196,517,546,868,901),
        (162,197,516,547,867,902),
        (161,198,515,548,866,903),
        (160,199,514,549,865,904),
        (159,200,513,550,864,905),
        (158,201,512,551,863,906),
        (157,202,511,552,862,907),
        (156,203,510,553,861,908),
        (155,204,509,554,860,909),
        (154,205,508,555,859,910),
        (153,206,507,556,858,911),
        (152,207,506,557,857,912),
        (151,208,505,558,856,913),
        (150,209,504,559,855,914),
        (149,210,503,560,854,915),
        (148,211,502,561,853,916),
        (147,212,501,562,852,917),
        (146,213,500,563,851,918),
        (145,214,499,564,850,919),
        (144,215,498,565,849,920),
        (143,216,497,566,848,921),
        (142,217,496,567,847,922),
        (141,218,495,568,846,923),
        (140,219,494,569,845,924),
        (139,220,493,570,844,925),
        (138,221,492,571,843,926),
        (137,222,491,572,842,927),
        (136,223,490,573,841,928),
        (135,224,489,574,840,929),
        (134,225,488,575,839,930),
        (133,226,487,576,838,931),
        (132,227,486,577,837,932),
        (131,228,485,578,836,933),
        (130,229,484,579,835,934),
        (129,230,483,580,834,935),
        (128,231,482,581,833,936),
        (127,232,481,582,832,937),
        (126,233,480,583,831,938),
        (125,234,479,584,830,939),
        (124,235,478,585,829,940),
        (123,236,477,586,828,941),
        (122,237,476,587,827,942),
        (121,238,475,588,826,943),
        (120,239,474,589,825,944),
        (119,240,473,590,824,945),
        (118,241,472,591,823,946),
        (117,242,471,592,822,947),
        (116,243,470,593,821,948),
        (115,244,469,594,820,949),
        (114,245,468,595,819,950),
        (113,246,467,596,818,951),
        (112,247,466,597,817,952),
        (111,248,465,598,816,953),
        (110,249,464,599,815,954),
        (109,250,463,600,814,955),
        (108,251,462,601,813,956),
        (107,252,461,602,812,957),
        (106,253,460,603,811,958),
        (105,254,459,604,810,959),
        (104,255,458,605,809,960),
        (103,256,457,606,808,961),
        (102,257,456,607,807,962),
        (101,258,455,608,806,963),
        (100,259,454,609,805,964),
        (99,260,453,610,804,965),
        (98,261,452,611,803,966),
        (97,262,451,612,802,967),
        (96,263,450,613,801,968),
        (95,264,449,614,800,969),
        (94,265,448,615,799,970),
        (93,266,447,616,798,971),
        (92,267,446,617,797,972),
        (91,268,445,618,796,973),
        (90,269,444,619,795,974),
        (89,270,443,620,794,975),
        (88,271,442,621,793,976),
        (87,272,441,622,792,977),
        (86,273,440,623,791,978),
        (85,274,439,624,790,979),
        (84,275,438,625,789,980),
        (83,276,437,626,788,981),
        (82,277,436,627,787,982),
        (81,278,435,628,786,983),
        (80,279,434,629,785,984),
        (79,280,433,630,784,985),
        (78,281,432,631,783,986),
        (77,282,431,632,782,987),
        (76,283,430,633,781,988),
        (75,284,429,634,780,989),
        (74,285,428,635,779,990),
        (73,286,427,636,778,991),
        (72,287,426,637,777,992),
        (71,288,425,638,776,993),
        (70,289,424,639,775,994),
        (69,290,423,640,774,995),
        (68,291,422,641,773,996),
        (67,292,421,642,772,997),
        (66,293,420,643,771,998),
        (65,294,419,644,770,999),
        (64,295,418,645,769,1000),
        (63,296,417,646,768,1001),
        (62,297,416,647,767,1002),
        (61,298,415,648,766,1003),
        (60,299,414,649,765,1004),
        (59,300,413,650,764,1005),
        (58,301,412,651,763,1006),
        (57,302,411,652,762,1007),
        (56,303,410,653,761,1008),
        (55,304,409,654,760,1009),
        (54,305,408,655,759,1010),
        (53,306,407,656,758,1011),
        (52,307,406,657,757,1012),
        (51,308,405,658,756,1013),
        (50,309,404,659,755,1014),
        (49,310,403,660,754,1015),
        (48,311,402,661,753,1016),
        (47,312,401,662,752,1017),
        (46,313,400,663,751,1018),
        (45,314,399,664,750,1019),
        (44,315,398,665,749,1020),
        (43,316,397,666,748,1021),
        (42,317,396,667,747,1022),
        (41,318,395,668,746,1023),
        (40,319,394,669,745,1024),
        (39,320,393,670,744,1025),
        (38,321,392,671,743,1026),
        (37,322,391,672,742,1027),
        (36,323,390,673,741,1028),
        (35,324,389,674,740,1029),
        (34,325,388,675,739,1030),
        (33,326,387,676,738,1031),
        (32,327,386,677,737,1032),
        (31,328,385,678,736,1033),
        (30,329,384,679,735,1034),
        (29,330,383,680,734,1035),
        (28,331,382,681,733,1036),
        (27,332,381,682,732,1037),
        (26,333,380,683,731,1038),
        (25,334,379,684,730,1039),
        (24,335,378,685,729,1040),
        (23,336,377,686,728,1041),
        (22,337,376,687,727,1042),
        (21,338,375,688,726,1043),
        (20,339,374,689,725,1044),
        (19,340,373,690,724,1045),
        (18,341,372,691,723,1046),
        (17,342,371,692,722,1047),
        (16,343,370,693,721,1048),
        (15,344,369,694,720,1049),
        (14,345,368,695,719,1050),
        (13,346,367,696,718,1051),
        (12,347,366,697,717,1052),
        (11,348,365,698,716,1053),
        (10,349,364,699,715,1054),
        (9,350,363,700,714,1055),
        (8,351,362,701,713,1056),
        (7,352,361,702,712,1057),
        (6,353,360,703,711,1058),
        (5,354,359,704,710,1059),
        (4,355,358,705,709,1060),
        (3,356,357,706,708,1061),
        (2,357,356,707,707,1062),
        (1,358,355,708,706,1063),
        (0,359,354,709,705,1064),

    ]
    
    

