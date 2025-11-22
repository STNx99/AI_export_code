import React from "react";
import { SectionComponent, DivComponent, TextComponent, ImageComponent } from "./index";

export default function Section1() {
  return (
    <>
      <SectionComponent styles={{}} className="w-full py-14 px-4 md:px-8">
        <DivComponent styles={{}} className="max-w-4xl mx-auto flex flex-col gap-4">
          <DivComponent styles={{}} className="p-4 rounded-lg bg-transparent border border-border" />
        </DivComponent>
      </SectionComponent>
    </>
  );
}