"""empty message

Revision ID: 49e791063766
Revises: 42ecd75e599d
Create Date: 2021-12-01 00:26:25.833642

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "49e791063766"
down_revision = "42ecd75e599d"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("course", sa.Column("survey_count", sa.Integer(), nullable=True))
    op.add_column("course", sa.Column("scale_factor", sa.FLOAT(), nullable=True))
    op.drop_constraint("course_survey_config_fkey", "course", type_="foreignkey")
    op.drop_column("course", "survey_config")
    op.add_column(
        "individual_score", sa.Column("score_qlt_individual", sa.FLOAT(), nullable=True)
    )
    op.add_column(
        "individual_score", sa.Column("score_qnt_individual", sa.FLOAT(), nullable=True)
    )
    op.add_column(
        "individual_score", sa.Column("score_qlt_team", sa.FLOAT(), nullable=True)
    )
    op.add_column(
        "individual_score", sa.Column("score_qnt_team", sa.FLOAT(), nullable=True)
    )
    op.add_column(
        "individual_score", sa.Column("score_ability", sa.FLOAT(), nullable=True)
    )
    op.add_column(
        "individual_score", sa.Column("score_effort", sa.FLOAT(), nullable=True)
    )
    op.add_column(
        "individual_score", sa.Column("score_significant", sa.FLOAT(), nullable=True)
    )
    op.add_column(
        "individual_score", sa.Column("score_attitude", sa.FLOAT(), nullable=True)
    )
    op.add_column("individual_score", sa.Column("iwf", sa.FLOAT(), nullable=True))
    op.drop_constraint("survey_survey_config_fkey", "survey", type_="foreignkey")
    op.drop_column("survey", "survey_config")
    op.drop_table("survey_config")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "survey",
        sa.Column("survey_config", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.create_foreign_key(
        "survey_survey_config_fkey",
        "survey",
        "survey_config",
        ["survey_config"],
        ["id"],
    )
    op.drop_column("individual_score", "iwf")
    op.drop_column("individual_score", "score_attitude")
    op.drop_column("individual_score", "score_significant")
    op.drop_column("individual_score", "score_effort")
    op.drop_column("individual_score", "score_ability")
    op.drop_column("individual_score", "score_qnt_team")
    op.drop_column("individual_score", "score_qlt_team")
    op.drop_column("individual_score", "score_qnt_individual")
    op.drop_column("individual_score", "score_qlt_individual")
    op.add_column(
        "course",
        sa.Column("survey_config", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.create_foreign_key(
        "course_survey_config_fkey",
        "course",
        "survey_config",
        ["survey_config"],
        ["id"],
    )
    op.drop_column("course", "scale_factor")
    op.drop_column("course", "survey_count")
    op.create_table(
        "survey_config",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("course", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("survey_count", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column(
            "scale_factor",
            postgresql.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["course"], ["course.id"], name="survey_config_course_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="survey_config_pkey"),
    )
    # ### end Alembic commands ###