import React from "react";
import { SectionComponent, DivComponent, TextComponent, ImageComponent } from "./index";

export default function Section2() {
  return (
    <>
      <SectionComponent styles={{}} className="w-full py-14 px-4 md:px-8">
        <DivComponent styles={{}} className="max-w-4xl mx-auto flex flex-col gap-4">
          <DivComponent styles={{}} className="p-4 rounded-lg bg-transparent border border-border">
            <TextComponent content="How quickly can I launch a site?" styles={{}} className="font-semibold text-foreground" />
            <TextComponent content="You can launch a simple site in minutes using templates." styles={{}} className="text-sm text-muted-foreground mt-2" />
          </DivComponent>
          <DivComponent styles={{}} className="p-4 rounded-lg bg-transparent border border-border">
            <TextComponent content="Can I export code?" styles={{}} className="font-semibold text-foreground" />
            <TextComponent content="Yes — export static assets or connect your preferred hosting in a few clicks." styles={{}} className="text-sm text-muted-foreground mt-2" />
          </DivComponent>
          <DivComponent styles={{}} className="p-4 rounded-lg bg-transparent border border-border">
            <TextComponent content="Is there a free tier?" styles={{}} className="font-semibold text-foreground" />
            <TextComponent content="Yes, our Starter plan is free for individual use and testing." styles={{}} className="text-sm text-muted-foreground mt-2" />
          </DivComponent>
        </DivComponent>
      </SectionComponent>
    </>
  );
}