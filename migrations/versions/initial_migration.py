from alembic import op
import sqlalchemy as sa

revision = '1a2b3c4d5e6f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'usuarios',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('nombre', sa.String(length=100), nullable=False),
        sa.Column('apellido', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('hashed_password', sa.String(length=100), nullable=False),
        sa.Column('fecha_registro', sa.DateTime(), nullable=False),
        sa.Column('activo', sa.Boolean(), nullable=False, default=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    op.create_table(
        'parcelas',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('nombre', sa.String(length=100), nullable=False),
        sa.Column('ubicacion', sa.String(length=200), nullable=True),
        sa.Column('superficie', sa.Float(), nullable=True),
        sa.Column('usuario_id', sa.Integer(), nullable=False),
        sa.Column('fecha_registro', sa.DateTime(), nullable=False),
        sa.Column('activo', sa.Boolean(), nullable=False, default=True),
        sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'cultivos',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('nombre', sa.String(length=100), nullable=False),
        sa.Column('variedad', sa.String(length=100), nullable=True),
        sa.Column('fecha_siembra', sa.Date(), nullable=True),
        sa.Column('fecha_cosecha_estimada', sa.Date(), nullable=True),
        sa.Column('parcela_id', sa.Integer(), nullable=False),
        sa.Column('fecha_registro', sa.DateTime(), nullable=False),
        sa.Column('activo', sa.Boolean(), nullable=False, default=True),
        sa.ForeignKeyConstraint(['parcela_id'], ['parcelas.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'productos_fitosanitarios',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('nombre', sa.String(length=100), nullable=False),
        sa.Column('tipo', sa.String(length=50), nullable=False),
        sa.Column('fabricante', sa.String(length=100), nullable=True),
        sa.Column('principio_activo', sa.String(length=100), nullable=True),
        sa.Column('dosis_recomendada', sa.String(length=100), nullable=True),
        sa.Column('periodo_carencia', sa.Integer(), nullable=True),
        sa.Column('usuario_id', sa.Integer(), nullable=False),
        sa.Column('fecha_registro', sa.DateTime(), nullable=False),
        sa.Column('activo', sa.Boolean(), nullable=False, default=True),
        sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'aplicaciones',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('fecha_aplicacion', sa.Date(), nullable=False),
        sa.Column('producto_id', sa.Integer(), nullable=False),
        sa.Column('cultivo_id', sa.Integer(), nullable=False),
        sa.Column('dosis_aplicada', sa.Float(), nullable=False),
        sa.Column('unidad_medida', sa.String(length=20), nullable=False),
        sa.Column('area_tratada', sa.Float(), nullable=True),
        sa.Column('motivo', sa.String(length=200), nullable=True),
        sa.Column('observaciones', sa.Text(), nullable=True),
        sa.Column('fecha_segura_reingreso', sa.Date(), nullable=True),
        sa.Column('usuario_id', sa.Integer(), nullable=False),
        sa.Column('fecha_registro', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['producto_id'], ['productos_fitosanitarios.id'], ),
        sa.ForeignKeyConstraint(['cultivo_id'], ['cultivos.id'], ),
        sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'recordatorios',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('aplicacion_id', sa.Integer(), nullable=False),
        sa.Column('fecha_recordatorio', sa.Date(), nullable=False),
        sa.Column('tipo', sa.String(length=50), nullable=False),
        sa.Column('mensaje', sa.String(length=200), nullable=False),
        sa.Column('completado', sa.Boolean(), nullable=False, default=False),
        sa.Column('fecha_registro', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['aplicacion_id'], ['aplicaciones.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('recordatorios')
    op.drop_table('aplicaciones')
    op.drop_table('productos_fitosanitarios')
    op.drop_table('cultivos')
    op.drop_table('parcelas')
    op.drop_table('usuarios')
