PGDMP      0    	            }         
   mind_drone    16.1    16.1 #               0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            	           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            
           1262    16398 
   mind_drone    DATABASE     �   CREATE DATABASE mind_drone WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_United States.1252';
    DROP DATABASE mind_drone;
                postgres    false            �            1259    16407    command    TABLE     �   CREATE TABLE public.command (
    command_id integer NOT NULL,
    x_control double precision NOT NULL,
    y_control double precision NOT NULL,
    z_control double precision NOT NULL,
    time_duration double precision NOT NULL
);
    DROP TABLE public.command;
       public         heap    postgres    false            �            1259    16406    command_command_id_seq    SEQUENCE     �   CREATE SEQUENCE public.command_command_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.command_command_id_seq;
       public          postgres    false    218                       0    0    command_command_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.command_command_id_seq OWNED BY public.command.command_id;
          public          postgres    false    217            �            1259    16431 	   mind_user    TABLE     �   CREATE TABLE public.mind_user (
    user_id integer NOT NULL,
    model_id integer,
    first_name character varying(50) NOT NULL,
    last_name character varying(50) NOT NULL
);
    DROP TABLE public.mind_user;
       public         heap    postgres    false            �            1259    16430    mind_user_user_id_seq    SEQUENCE     �   CREATE SEQUENCE public.mind_user_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public.mind_user_user_id_seq;
       public          postgres    false    222                       0    0    mind_user_user_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public.mind_user_user_id_seq OWNED BY public.mind_user.user_id;
          public          postgres    false    221            �            1259    16414    training_model    TABLE     s   CREATE TABLE public.training_model (
    model_id integer NOT NULL,
    wave_id integer,
    command_id integer
);
 "   DROP TABLE public.training_model;
       public         heap    postgres    false            �            1259    16413    training_model_model_id_seq    SEQUENCE     �   CREATE SEQUENCE public.training_model_model_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 2   DROP SEQUENCE public.training_model_model_id_seq;
       public          postgres    false    220                       0    0    training_model_model_id_seq    SEQUENCE OWNED BY     [   ALTER SEQUENCE public.training_model_model_id_seq OWNED BY public.training_model.model_id;
          public          postgres    false    219            �            1259    16400    wave    TABLE     �   CREATE TABLE public.wave (
    wave_id integer NOT NULL,
    wave_type character varying(50) NOT NULL,
    frequency double precision NOT NULL,
    amplitude double precision NOT NULL,
    power double precision NOT NULL
);
    DROP TABLE public.wave;
       public         heap    postgres    false            �            1259    16399    wave_wave_id_seq    SEQUENCE     �   CREATE SEQUENCE public.wave_wave_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.wave_wave_id_seq;
       public          postgres    false    216                       0    0    wave_wave_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.wave_wave_id_seq OWNED BY public.wave.wave_id;
          public          postgres    false    215            `           2604    16410    command command_id    DEFAULT     x   ALTER TABLE ONLY public.command ALTER COLUMN command_id SET DEFAULT nextval('public.command_command_id_seq'::regclass);
 A   ALTER TABLE public.command ALTER COLUMN command_id DROP DEFAULT;
       public          postgres    false    217    218    218            b           2604    16434    mind_user user_id    DEFAULT     v   ALTER TABLE ONLY public.mind_user ALTER COLUMN user_id SET DEFAULT nextval('public.mind_user_user_id_seq'::regclass);
 @   ALTER TABLE public.mind_user ALTER COLUMN user_id DROP DEFAULT;
       public          postgres    false    221    222    222            a           2604    16417    training_model model_id    DEFAULT     �   ALTER TABLE ONLY public.training_model ALTER COLUMN model_id SET DEFAULT nextval('public.training_model_model_id_seq'::regclass);
 F   ALTER TABLE public.training_model ALTER COLUMN model_id DROP DEFAULT;
       public          postgres    false    219    220    220            _           2604    16403    wave wave_id    DEFAULT     l   ALTER TABLE ONLY public.wave ALTER COLUMN wave_id SET DEFAULT nextval('public.wave_wave_id_seq'::regclass);
 ;   ALTER TABLE public.wave ALTER COLUMN wave_id DROP DEFAULT;
       public          postgres    false    215    216    216                       0    16407    command 
   TABLE DATA           ]   COPY public.command (command_id, x_control, y_control, z_control, time_duration) FROM stdin;
    public          postgres    false    218   3(                 0    16431 	   mind_user 
   TABLE DATA           M   COPY public.mind_user (user_id, model_id, first_name, last_name) FROM stdin;
    public          postgres    false    222   P(                 0    16414    training_model 
   TABLE DATA           G   COPY public.training_model (model_id, wave_id, command_id) FROM stdin;
    public          postgres    false    220   m(       �          0    16400    wave 
   TABLE DATA           O   COPY public.wave (wave_id, wave_type, frequency, amplitude, power) FROM stdin;
    public          postgres    false    216   �(                  0    0    command_command_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.command_command_id_seq', 1, false);
          public          postgres    false    217                       0    0    mind_user_user_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.mind_user_user_id_seq', 1, false);
          public          postgres    false    221                       0    0    training_model_model_id_seq    SEQUENCE SET     J   SELECT pg_catalog.setval('public.training_model_model_id_seq', 1, false);
          public          postgres    false    219                       0    0    wave_wave_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.wave_wave_id_seq', 1, false);
          public          postgres    false    215            f           2606    16412    command command_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.command
    ADD CONSTRAINT command_pkey PRIMARY KEY (command_id);
 >   ALTER TABLE ONLY public.command DROP CONSTRAINT command_pkey;
       public            postgres    false    218            j           2606    16436    mind_user mind_user_pkey 
   CONSTRAINT     [   ALTER TABLE ONLY public.mind_user
    ADD CONSTRAINT mind_user_pkey PRIMARY KEY (user_id);
 B   ALTER TABLE ONLY public.mind_user DROP CONSTRAINT mind_user_pkey;
       public            postgres    false    222            h           2606    16419 "   training_model training_model_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.training_model
    ADD CONSTRAINT training_model_pkey PRIMARY KEY (model_id);
 L   ALTER TABLE ONLY public.training_model DROP CONSTRAINT training_model_pkey;
       public            postgres    false    220            d           2606    16405    wave wave_pkey 
   CONSTRAINT     Q   ALTER TABLE ONLY public.wave
    ADD CONSTRAINT wave_pkey PRIMARY KEY (wave_id);
 8   ALTER TABLE ONLY public.wave DROP CONSTRAINT wave_pkey;
       public            postgres    false    216            m           2606    16437 !   mind_user mind_user_model_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.mind_user
    ADD CONSTRAINT mind_user_model_id_fkey FOREIGN KEY (model_id) REFERENCES public.training_model(model_id) ON DELETE CASCADE;
 K   ALTER TABLE ONLY public.mind_user DROP CONSTRAINT mind_user_model_id_fkey;
       public          postgres    false    220    4712    222            k           2606    16425 -   training_model training_model_command_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.training_model
    ADD CONSTRAINT training_model_command_id_fkey FOREIGN KEY (command_id) REFERENCES public.command(command_id) ON DELETE CASCADE;
 W   ALTER TABLE ONLY public.training_model DROP CONSTRAINT training_model_command_id_fkey;
       public          postgres    false    218    220    4710            l           2606    16420 *   training_model training_model_wave_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.training_model
    ADD CONSTRAINT training_model_wave_id_fkey FOREIGN KEY (wave_id) REFERENCES public.wave(wave_id) ON DELETE CASCADE;
 T   ALTER TABLE ONLY public.training_model DROP CONSTRAINT training_model_wave_id_fkey;
       public          postgres    false    4708    220    216                   x������ � �            x������ � �            x������ � �      �      x������ � �     