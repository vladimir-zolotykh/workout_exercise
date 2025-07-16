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

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}, id={self.id}, child_id={self.child_id}>"


class Child(Base):
    __tablename__ = "child_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    parents: Mapped[List["Parent"]] = relationship(back_populates="child")

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id} parents={self.parents!r}"


if __name__ == "__main__":
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        # echo=True,
        future=True,
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        p1 = Parent()
        p2 = Parent()
        p3 = Parent()
        c1 = Child()
        c1.parents.extend([p1, p2])
        session.add(c1)
        session.commit()
        print(p1, c1)
