#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from __future__ import annotations
from typing import List

from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship, Session


class Base(DeclarativeBase):
    pass


class Parent(Base):
    __tablename__ = "parent_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    children: Mapped[List[Child]] = relationship(back_populates="parent")

    def __repr__(self) -> str:  # just for nicer output
        return f"<Parent id={self.id} children={len(self.children)}>"


class Child(Base):
    __tablename__ = "child_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("parent_table.id"))
    parent: Mapped[Parent] = relationship(back_populates="children")

    def __repr__(self) -> str:
        return f"<Child id={self.id} parent_id={self.parent_id}>"


if __name__ == "__main__":
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        # echo=True,
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
