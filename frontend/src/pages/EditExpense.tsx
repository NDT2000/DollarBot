import React, { useEffect, useState } from "react";
import {
  Center,
  Container,
  createListCollection,
  Flex,
  Heading,
  Icon,
  Input,
  Text,
} from "@chakra-ui/react";
import {
  SelectContent,
  SelectItem,
  SelectLabel,
  SelectRoot,
  SelectTrigger,
  SelectValueText,
} from "../components/ui/select";
import { Button } from "../components/ui/button";
import { useForm } from "react-hook-form";
import { FaDollarSign } from "react-icons/fa";
import { FaEuroSign } from "react-icons/fa";
import { FaIndianRupeeSign } from "react-icons/fa6";
import {
  NumberInputField,
  NumberInputRoot,
} from "../components/ui/number-input";
import type { DatePickerProps } from "antd";
import { DatePicker, Space } from "antd";
import axios from "axios";
import dayjs from "dayjs";

type Props = {
  onEditExpense?: (value: boolean) => void;
  selectedExpense: string[];
};

type expenseProps = {
  expense_date: string;
  expense_category: string;
  expense_amount: string;
};

const EditExpense = ({ onEditExpense, selectedExpense }: Props) => {
  const {
    handleSubmit,
    register,
    formState: { errors, isSubmitting },
  } = useForm();

  const date = new Date();

  let day = date.getDate();
  let month = date.getMonth() + 1;
  let year = date.getFullYear();

  const [expDate, setExpDate] = useState(`${year}-${month}-${day}`);
  const [expenseValue, setExpenseValue] = useState("0");
  const [expenseCategory, setExpenseCategory] = useState("");
  const [oldData, setOldData] = useState<expenseProps>({
    expense_amount: "0",
    expense_category: "",
    expense_date: `${year}-${month}-${day}`,
  });

  async function onSubmit(data: any) {
    if (selectedExpense.length == 1) {
      await axios.post(
        "http://127.0.0.1:5000/edit_cost",
        {
          user_id: "864914213",
          new_cost: expenseValue,
          selected_data: [
            "Date=" + oldData.expense_date,
            "Category=" + oldData.expense_category,
            "Amount=" + oldData.expense_amount,
          ],
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      await axios.post(
        "http://127.0.0.1:5000/edit_date",
        {
          user_id: "864914213",
          new_date: expDate,
          selected_data: [
            "Date=" + oldData.expense_date,
            "Category=" + oldData.expense_category,
            "Amount=" + oldData.expense_amount,
          ],
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      await axios.post(
        "http://127.0.0.1:5000/edit_category",
        {
          user_id: "864914213",
          new_category: expenseCategory,
          selected_data: [
            "Date=" + oldData.expense_date,
            "Category=" + oldData.expense_category,
            "Amount=" + oldData.expense_amount,
          ],
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
    }
    setOldData({
        expense_amount:expenseValue,
        expense_category:expenseCategory,
        expense_date:expDate
    })
    await new Promise((r) => setTimeout(r, 2000));
    onEditExpense?.(true);
  }

  useEffect(() => {
    if (selectedExpense.length == 1) {
      axios
        .get("http://127.0.0.1:5000/display/864914213")
        .then(function (resp) {
          for (let i = 0; i < resp.data.length; i++) {
            var expenseData: expenseProps = {
              expense_amount: "0",
              expense_category: "",
              expense_date: `${year}-${month}-${day}`,
            };
            if (i == parseInt(selectedExpense[0])) {
              expenseData = {
                expense_amount: resp.data[i]["expense_amount"],
                expense_category: resp.data[i]["expense_category"],
                expense_date: resp.data[i]["expense_date"],
              };
              if (selectedExpense.length == 1) {
                setOldData(expenseData);
                setExpenseValue(expenseData.expense_amount);
                setExpenseCategory(expenseData.expense_category);
                setExpDate(expenseData.expense_date);
              }
            }
          }
        });
    } else {
      setExpDate(`${year}-${month}-${day}`);
      setExpenseCategory("");
      setExpenseValue("0");
    }
  }, [selectedExpense]);

  return (
    <Container>
      <Center>
        <Heading fontWeight="bold" marginBottom="10px">
          Edit Expenses
        </Heading>
      </Center>
      <Text fontSize="sm" marginBottom="10px" fontWeight="bold" color="teal">
        Select one transaction from the table to edit.
      </Text>
      <form onSubmit={handleSubmit(onSubmit)}>
        <Text fontSize="sm" fontWeight="medium" marginBottom="2px">
          Edit Date
        </Text>
        <DatePicker
          size="large"
          value={dayjs(expDate, "YYYY-MM-DD")}
          style={{ width: "100%", marginBottom: "10px" }}
          onChange={(dateStrings) => {
            if (dateStrings != null) {
              setExpDate(String(dateStrings.format("YYYY-MM-DD")));
            }
          }}
        />
        <Text fontSize="sm" fontWeight="medium" marginBottom="2px">
          Edit Category
        </Text>
        <Input
          id="category"
          marginBottom="10px"
          placeholder="Enter Category"
          value={expenseCategory}
          onChange={(e: any) => {
            setExpenseCategory(String(e.target.value));
          }}
        />
        <Text fontSize="sm" fontWeight="medium" marginBottom="2px">
          Edit Expense Value
        </Text>
        <Flex flexDir="row">
          <SelectRoot
            collection={currencies}
            size="md"
            width="65px"
            variant="subtle"
            margin="0 5px 0px 0"
            defaultValue={["dollar"]}
          >
            <SelectTrigger>
              <SelectValueText color="teal" placeholder="Select Action" />
            </SelectTrigger>
            <SelectContent>
              {currencies.items.map((currency) => (
                <SelectItem color="teal" item={currency} key={currency.value}>
                  {currency.label}
                </SelectItem>
              ))}
            </SelectContent>
          </SelectRoot>
          <NumberInputRoot
            size="md"
            defaultValue="0"
            marginBottom="10px"
            min={0}
            height="100%"
            onValueChange={({ value }) => {
              setExpenseValue(value);
            }}
          >
            <NumberInputField value={expenseValue} />
          </NumberInputRoot>
        </Flex>
        <Button mt={4} colorScheme="teal" loading={isSubmitting} type="submit">
          Edit
        </Button>
      </form>
    </Container>
  );
};

const currencies = createListCollection({
  items: [
    {
      label: (
        <Icon>
          <FaDollarSign />
        </Icon>
      ),
      value: "dollar",
    },
    {
      label: (
        <Icon>
          <FaEuroSign />
        </Icon>
      ),
      value: "euro",
    },
    {
      label: (
        <Icon>
          <FaIndianRupeeSign />
        </Icon>
      ),
      value: "rupee",
    },
  ],
});

export default EditExpense;
