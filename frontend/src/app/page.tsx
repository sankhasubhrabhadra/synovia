export const dynamic = "force-dynamic";
export const fetchCache = "force-no-store";
export const revalidate = 0;

import React from "react";
import { SynoviaApp } from "@/components/SynoviaApp";

export default function Home() {
  return <SynoviaApp />;
}
