import { Button } from "../components/ui/button";
import {
  Card,
  Container,
  AbsoluteCenter,
  HStack,
  Input,
  Stack,
  Center,
  Flex,
  Text,
  Link,
  Table,
  ActionBarContent,
  ActionBarRoot,
  ActionBarSelectionTrigger,
  ActionBarSeparator,
  createListCollection,
  Kbd,
  Box,
  ListCollection,
} from "@chakra-ui/react";
import { Field } from "../components/ui/field";
import { Checkbox } from "../components/ui/checkbox";
import { PasswordInput } from "../components/ui/password-input";
import { useState } from "react";
import {
  SelectContent,
  SelectItem,
  SelectLabel,
  SelectRoot,
  SelectTrigger,
  SelectValueText,
} from "../components/ui/select";
import React from "react";
import AddExpense from "./AddExpense";
import EditExpense from "./EditExpense";
import DeleteExpense from "./DeleteExpense";
import axios from "axios";
import { useEffect } from "react";

const Home = () => {
  const [visible, setVisible] = useState(false);
  const [selection, setSelection] = useState<string[]>([]);
  const [action, setAction] = useState<string>("add");
  const [expenses, setExpenses] = useState([{}]);

  const handleExpense = (value: boolean) => {
    if (value) {
      var newData: any[] = [];
      axios
        .get("http://127.0.0.1:5000/display/864914213")
        .then(function (resp) {
          for (let i = 0; i < resp.data.length; i++) {
            const expenseData = {
              expense_amount: resp.data[i]["expense_amount"],
              expense_category: resp.data[i]["expense_category"],
              expense_date: resp.data[i]["expense_date"],
            };
            newData.push(expenseData);
          }
          setExpenses(newData);
        });
    }
  };

  useEffect(() => {
    var newData: any[] = [];
    axios.get("http://127.0.0.1:5000/display/864914213").then(function (resp) {
      for (let i = 0; i < resp.data.length; i++) {
        const expenseData = {
          id: i,
          expense_amount: resp.data[i]["expense_amount"],
          expense_category: resp.data[i]["expense_category"],
          expense_date: resp.data[i]["expense_date"],
        };
        newData.push(expenseData);
      }
      setExpenses(newData);
    });
  }, [selection]);

  const hasSelection = selection.length > 0;
  const indeterminate = hasSelection && selection.length < expenses.length;

  const renderSwitch = (action: string) => {
    switch (action) {
      case "add":
        return <AddExpense onAddExpense={handleExpense} />;
      case "edit":
        return <EditExpense onEditExpense={handleExpense} selectedExpense={selection}/>;
      case "delete":
        return <DeleteExpense onDeleteExpense={handleExpense} selectedExpense={selection}/>;
    }
  };

  const rows = expenses.map((item: any) => (
    <Table.Row
      key={item["id"]}
      //   data-selected={selection.includes(item["expense_date"]) ? "" : undefined}
    >
      <Table.Cell>
        <Checkbox
          top="1"
          aria-label="Select row"
          checked={selection.includes(item["id"])}
          onCheckedChange={(changes) => {
            setSelection((prev) =>
              changes.checked
                ? [...prev, item["id"]]
                : selection.filter((date) => date !== item["id"])
            );
          }}
        />
      </Table.Cell>
      <Table.Cell>{item["expense_date"]}</Table.Cell>
      <Table.Cell>{item["expense_category"]}</Table.Cell>
      <Table.Cell>{item["expense_amount"]}</Table.Cell>
    </Table.Row>
  ));

  return (
    <div>
      <Container>
        <Flex justifyContent="flex-start" color="black">
          <Text
            color="teal"
            textStyle="3xl"
            fontWeight="bold"
            margin="12px 90px 0 0"
          >
            Dollar Bot
          </Text>
          <Link
            color="black"
            textStyle="lg"
            href="/"
            fontWeight="medium"
            margin="18px 35px 0 0"
          >
            Log Out
          </Link>
          <Link
            color="black"
            textStyle="lg"
            fontWeight="medium"
            margin="18px 35px 0 0"
            href="https://github.com/SoftwareEngNoobs/DollarBot"
          >
            About
          </Link>
          <Link
            color="black"
            textStyle="lg"
            fontWeight="medium"
            margin="18px 35px 0 0"
            href="https://github.com/SoftwareEngNoobs/DollarBot"
          >
            Help
          </Link>
        </Flex>
      </Container>
      <AbsoluteCenter
        alignContent="center"
        borderRadius="xl"
        axis="both"
        background="black"
      >
        <Flex
          overflow="hidden"
          borderRadius="xl"
          shadow="lg"
          padding="20px"
          divideX="2px"
          divideColor="#F2F0EF"
          divideStyle="dashed"
        >
          <Flex flexDir="column">
            <Container color="white" background="black">
              <SelectRoot
                collection={actions}
                size="sm"
                width="320px"
                defaultValue={["add"]}
                variant="subtle"
                margin="0 0 15px 0"
                onValueChange={({ value }) => setAction(value[0])}
              >
                <SelectLabel fontWeight="bold">Action</SelectLabel>
                <SelectTrigger>
                  <SelectValueText color="teal" placeholder="Select Action" />
                </SelectTrigger>
                <SelectContent>
                  {actions.items.map((action) => (
                    <SelectItem color="teal" item={action} key={action.value}>
                      {action.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </SelectRoot>
            </Container>
            <Box
              divideY="2px"
              marginBottom="10px"
              width="97%"
              divideColor="#F2F0EF"
            >
              <Box></Box>
              <Box></Box>
            </Box>
            {renderSwitch(action)}
          </Flex>
          <Table.Root borderRadius="xl" size="md" width="400px">
            <Table.Header>
              <Table.Row>
                <Table.ColumnHeader w="6">
                  <Checkbox
                    top="1"
                    aria-label="Select all rows"
                    checked={
                      indeterminate ? "indeterminate" : selection.length > 0
                    }
                    onCheckedChange={(changes) => {
                      setSelection(
                        changes.checked
                          ? expenses.map((item: any) => item["id"])
                          : []
                      );
                    }}
                  />
                </Table.ColumnHeader>
                <Table.ColumnHeader fontWeight="extrabold">
                  Date
                </Table.ColumnHeader>
                <Table.ColumnHeader fontWeight="extrabold">
                  Category
                </Table.ColumnHeader>
                <Table.ColumnHeader fontWeight="extrabold">
                  Expense
                </Table.ColumnHeader>
              </Table.Row>
            </Table.Header>
            <Table.Body>{rows}</Table.Body>
          </Table.Root>
        </Flex>
      </AbsoluteCenter>
    </div>
  );
};

const actions = createListCollection({
  items: [
    { label: "Add", value: "add" },
    { label: "Edit", value: "edit" },
    { label: "Delete", value: "delete" },
    { label: "View", value: "view" },
  ],
});

export default Home;
