--
-- PostgreSQL database dump
--

-- Started on 2009-11-16 17:41:02 VET

SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

--
-- TOC entry 1828 (class 0 OID 0)
-- Dependencies: 1554
-- Name: comun_pais_id_seq; Type: SEQUENCE SET; Schema: public; Owner: esmayoy
--

SELECT pg_catalog.setval('comun_pais_id_seq', 141, true,1);


--
-- TOC entry 1825 (class 0 OID 63268)
-- Dependencies: 1555
-- Data for Name: comun_pais; Type: TABLE DATA; Schema: public; Owner: esmayoy
--

INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (1, 'Argentina',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (2, 'Bolivia',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (3, 'Brasil',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (4, 'Chile',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (5, 'Colombia',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (6, 'Costa Rica',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (7, 'Cuba',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (8, 'Ecuador',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (9, 'El Salvador',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (10, 'Guatemala',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (11, 'Guyana',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (12, 'Haití',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (13, 'Honduras',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (14, 'México',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (15, 'Nicaragua',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (16, 'Panamá',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (17, 'Paraguay',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (18, 'Perú',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (19, 'Puerto Rico',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (20, 'Rep. Dominicana',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (21, 'Surinam',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (22, 'Uruguay',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (23, 'Venezuela',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (24, 'Canadá',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (25, 'Estados Unidos',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (26, 'Alemania',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (27, 'Andorra',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (28, 'Austria',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (29, 'Bélgica',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (30, 'Bosnia Herzegovina',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (31, 'Bulgaria',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (32, 'Ciudad del Vaticano',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (33, 'Dinamarca',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (34, 'Escocia',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (35, 'España',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (36, 'Finlandia',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (37, 'Francia',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (38, 'Grecia',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (39, 'Holanda',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (40, 'Hungria',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (41, 'Irlanda',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (42, 'Italia',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (43, 'Luxemburgo',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (44, 'Malta',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (45, 'Mónaco',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (46, 'Noruega',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (47, 'Polonia',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (48, 'Portugal',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (49, 'Principado de Liechtenstein',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (50, 'Reino Unido',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (51, 'Rep. Checa',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (52, 'Rep. de Croatia',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (53, 'Rep. de Estonia',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (54, 'Rep. de Georgia',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (55, 'Rep. de Lithuania',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (56, 'Rep. de Slovenia',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (57, 'Rep. de Eslovaquia',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (58, 'Rumania',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (59, 'San Marino',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (60, 'Suecia',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (61, 'Suiza',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (62, 'Ucrania',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (63, 'Yugoslavia',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (64, 'Antillas Holandesas',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (65, 'Aruba',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (66, 'Bahamas',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (67, 'Barbados',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (68, 'Bermuda',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (69, 'Grenada',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (70, 'Jamaica',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (71, 'Martinique',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (72, 'Trinidad y Tobago',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (73, 'Afghanistán',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (74, 'Albania',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (75, 'Argelia',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (76, 'Angola',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (77, 'Arabia Saudita',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (78, 'Australia',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (79, 'Bangladesh',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (80, 'Cambodia',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (81, 'Camerún',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (82, 'China',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (83, 'Congo',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (84, 'Egipto',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (85, 'Emiratos Arabes Unidos',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (86, 'Etiopía',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (87, 'Filipinas',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (88, 'Ghana',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (89, 'Gibraltar',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (90, 'Groenlandia',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (91, 'Guinea',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (92, 'India',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (93, 'Indonesia',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (94, 'Irán',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (95, 'Iraq',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (96, 'Islandia',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (97, 'Israel',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (98, 'Japón',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (99, 'Kenya',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (100, 'Korea',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (101, 'Kuwait',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (102, 'Líbano',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (103, 'Liberia',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (104, 'Libia',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (105, 'Madagascar',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (106, 'Malaysia',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (107, 'Marruecos',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (108, 'Mauritania',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (109, 'Mongolia',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (110, 'Mozambique',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (111, 'Namibia',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (112, 'Nepal',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (113, 'Nigeria',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (114, 'Nueva Zelanda',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (115, 'Pakistán',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (116, 'Polinesia Francesa',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (117, 'Rep. Central Africana',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (118, 'Rep. de Armenia',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (119, 'Rep. de Belarusia',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (120, 'Rep. de China',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (121, 'Rep. de Korea',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (122, 'Rep. de Moldova',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (123, 'Rusia',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (124, 'Sahara Oriental',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (125, 'Senegal',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (126, 'Singapur',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (127, 'Siria',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (128, 'Somalia',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (129, 'Sudán',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (130, 'Sur Africa',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (131, 'Swazilandia',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (132, 'Tailandia',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (133, 'Tunisia',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (134, 'Turkmenistán',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (135, 'Turquía',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (136, 'Uganda',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (137, 'Viet Nam',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (138, 'Yemen',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (139, 'Zaire',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (140, 'Zambia',1);
INSERT INTO comun_pais (id, nombre,id_usuario)  VALUES (141, 'Zimbabwe',1);


-- Completed on 2009-11-16 17:41:03 VET

--
-- PostgreSQL database dump complete
--

