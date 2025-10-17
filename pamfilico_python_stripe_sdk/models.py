"""Pydantic models for Stripe SDK responses."""

from typing import Dict, Any, List
from pydantic import BaseModel, Field, EmailStr


class CustomerCreateInput(BaseModel):
    """Input model for creating a Stripe customer."""

    email: EmailStr | None = Field(None, description="Customer email address")
    name: str | None = Field(None, min_length=1, max_length=255, description="Customer name")
    phone: str | None = Field(None, description="Customer phone number")
    description: str | None = Field(None, max_length=500, description="Customer description")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Customer metadata")


class CustomerUpdateInput(BaseModel):
    """Input model for updating a Stripe customer."""

    email: EmailStr | None = Field(None, description="Updated customer email address")
    name: str | None = Field(None, min_length=1, max_length=255, description="Updated customer name")
    phone: str | None = Field(None, description="Updated customer phone number")
    description: str | None = Field(None, max_length=500, description="Updated customer description")
    metadata: Dict[str, Any] | None = Field(None, description="Updated customer metadata")


class CustomerData(BaseModel):
    """Stripe customer data model."""

    id: str = Field(..., description="Stripe customer ID")
    email: str | None = Field(None, description="Customer email address")
    name: str | None = Field(None, description="Customer name")
    phone: str | None = Field(None, description="Customer phone number")
    created: int | None = Field(None, description="Unix timestamp of creation")
    balance: int | None = Field(None, description="Customer balance in cents")
    currency: str | None = Field(None, description="Customer currency")
    delinquent: bool | None = Field(None, description="Whether customer is delinquent")
    description: str | None = Field(None, description="Customer description")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Customer metadata")


class CustomerResponse(BaseModel):
    """Response model for single customer operations."""

    data: CustomerData = Field(..., description="Customer data")
    meta: Dict[str, Any] = Field(default_factory=dict, description="Response metadata")


class CustomerListMeta(BaseModel):
    """Metadata for customer list responses."""

    has_more: bool = Field(..., description="Whether more results exist for pagination")
    total_count: int = Field(..., description="Number of customers in current page")
    note: str | None = Field(None, description="Optional note or message about the results")


class CustomerListResponse(BaseModel):
    """Response model for list customers operation."""

    data: List[CustomerData] = Field(..., description="List of customers")
    meta: CustomerListMeta = Field(..., description="Pagination metadata")
