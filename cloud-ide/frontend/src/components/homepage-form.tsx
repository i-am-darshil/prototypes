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
  projectName: z.string().min(6).max(50),
  projectType: z.string().min(1).max(50),
  hostName: z.string().min(1).max(500),
})

export default function HomepageForm() {
  const router = useRouter()
  const { socket } = useWebSocket();
  // const [projectName, setProjectName] = useState<string>(generateRandomWords(2, 6));
  // const [hostName, setHostName] = useState<string>("");

  // 1. Define your form.
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      projectName: generateRandomWords(2, 6),
      projectType: "python",
      hostName: ""
    },
  })

  // 2. Define a submit handler.
  function onSubmit(values: z.infer<typeof formSchema>) {
    // Do something with the form values.
    // ✅ This will be type-safe and validated.
    console.log(values)
    if (!socket) return;
    socket.emit("create-project", {
      name: values.projectName,
      type: values.projectType,
      host: values.hostName,
    });
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
                <Input {...field} />
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
                <Select {...field}>
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

        <FormField
          control={form.control}
          name="hostName"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Host Name</FormLabel>
              <FormControl>
                <Input {...field} />
              </FormControl>
              <FormDescription>
                Connect your IDE to this docker host.
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
