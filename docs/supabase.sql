-- Tabla de lectores registrados desde libro.momentumhub.cloud.
-- La escribe n8n (con la service key), nunca el navegador.
-- No ejecutar sin revisarlo con Neto.

create table if not exists public.libro_lectores (
  id             bigint generated always as identity primary key,
  correo         text not null,
  nombre         text,
  origen         text not null check (origen in ('introduccion', 'ticket', 'ventas')),
  consentimiento boolean not null default false,
  utm_source     text,
  utm_medium     text,
  utm_campaign   text,
  pais           text,
  creado_en      timestamptz not null default now(),
  baja_en        timestamptz,
  unique (correo, origen)
);

-- Sin acceso público: solo la service key de n8n puede leer y escribir.
alter table public.libro_lectores enable row level security;
