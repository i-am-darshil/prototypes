'use client'
import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { z } from "zod"

import { Button } from "@/components/ui/button"
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

import { generateRandomWords } from "@/utils/utils"
import { useState } from "react";
import { useWebSocket } from "@/contexts/WebSocketContext"

import { useRouter } from 'next/navigation'

const formSchema = z.object({
  projectName: z.string().min(2).max(50),
  projectType: z.string().min(2).max(50),
})

export default function HomepageForm() {
  const router = useRouter()
  const { socket } = useWebSocket();
  const [projectName, setProjectName] = useState<string>(generateRandomWords(2, 6));

  // 1. Define your form.
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      projectName: projectName,
      projectType: "python"
    },
  })

  // 2. Define a submit handler.
  function onSubmit(values: z.infer<typeof formSchema>) {
    // Do something with the form values.
    // ✅ This will be type-safe and validated.
    console.log(values)
    if (!socket) return;
    socket.emit("create-project", values);
    router.push(`/project/${values.projectName}?projectType=${values.projectType}`)
  }


  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
        <FormField
          control={form.control}
          name="projectName"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Project Name</FormLabel>
              <FormControl>
                <Input {...field} value={projectName} onChange={(e) => {setProjectName(e.target.value)}} />
              </FormControl>
              <FormDescription>
                This is your public project name.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="projectType"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Project Type</FormLabel>
              <FormControl>
              <Select>
                <SelectTrigger className="w-full">
                  <SelectValue placeholder="Python" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="python">Python</SelectItem>
                  <SelectItem value="node">NodeJS</SelectItem>
                </SelectContent>
              </Select>
              </FormControl>
              <FormDescription>
                An environment will be setup accordingly.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">Submit</Button>
      </form>
    </Form>
  );
}
