"use client"
import * as React from 'react';
import Box from '@mui/material/Box';
import { SimpleTreeView } from '@mui/x-tree-view/SimpleTreeView';
import { TreeItem } from '@mui/x-tree-view/TreeItem';
import { useWebSocket } from "@/contexts/WebSocketContext"

export default function FileTreeView({project_name}: {project_name: string}) {

  const { socket } = useWebSocket();

  React.useEffect(() => {
    console.log(`socket?.id: ${socket?.id}`)
    socket?.emit("file-directory-request", {
      name: project_name
    })

    const handler = (data: any) => {
      console.log(`file-directory-response: ${JSON.stringify(data)}`)
      setFolderStructure(data.output)
    }

    socket?.on("file-directory-response", handler)

    return () => {
      socket?.off("file-directory-response", handler);
    };
  }, [socket, project_name])

  const [folderStructure, setFolderStructure] = React.useState<any>({});

  const onClickListener = (itemId: any) => {
    console.log(itemId)
    socket?.emit("file-selected-request", {
      name: project_name,
      filePath: `/${itemId}`
    })
  }

  const convertToTreeItems = (data: any, parentId = '') => {
    return Object.entries(data).map(([key, value], index) => {
      const itemId = `${parentId}/${key}`; // Create a unique itemId for each TreeItem
      if (value === null) {
        // It's a file (leaf node)
        return <TreeItem itemId={itemId} key={itemId} label={key} onClick={(e) => {
          onClickListener(itemId)
          console.log(e)
        }}/>;
      } else {
        // It's a folder (has children)
        return (
          <TreeItem itemId={itemId} key={itemId} label={key} onClick={(e) => {
            onClickListener(itemId)
            console.log(e)
          }}>
            {convertToTreeItems(value, itemId)}
          </TreeItem>
        );
      }
    });
  };

  return (
    <Box sx={{ minHeight: 352, minWidth: 250 }}>
      <SimpleTreeView>
      {convertToTreeItems(folderStructure, project_name)}
        {/* <TreeItem itemId="grid" label="Data Grid">
          <TreeItem itemId="grid-community" label="@mui/x-data-grid" />
          <TreeItem itemId="grid-pro" label="@mui/x-data-grid-pro" />
          <TreeItem itemId="grid-premium" label="@mui/x-data-grid-premium" />
        </TreeItem>
        <TreeItem itemId="pickers" label="Date and Time Pickers">
          <TreeItem itemId="pickers-community" label="@mui/x-date-pickers" />
          <TreeItem itemId="pickers-pro" label="@mui/x-date-pickers-pro" />
        </TreeItem>
        <TreeItem itemId="charts" label="Charts">
          <TreeItem itemId="charts-community" label="@mui/x-charts" />
        </TreeItem>
        <TreeItem itemId="tree-view" label="Tree View">
          <TreeItem itemId="tree-view-community" label="@mui/x-tree-view" />
        </TreeItem> */}
      </SimpleTreeView>
    </Box>
  );
}