#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import annotations
from typing import List
from typing import Optional

from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship, Session


class Base(DeclarativeBase):
    pass


class Parent(Base):
    __tablename__ = "parent_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    child_id: Mapped[Optional[int]] = mapped_column(ForeignKey("child_table.id"))
    child: Mapped[Optional["Child"]] = relationship(back_populates="parents")


class Child(Base):
    __tablename__ = "child_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    parents: Mapped[List["Parent"]] = relationship(back_populates="child")


if __name__ == "__main__":
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        echo=True,
        future=True,
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        p = Parent()
        c1 = Child()
        c2 = Child()
        p.children.append(c1)
        p.children.append(c2)
        session.add(p)
        session.commit()
        print(p.children)
        print(c1, c2)
